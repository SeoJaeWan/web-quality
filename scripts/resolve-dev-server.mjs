import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, "..");
const DEFAULT_URL = "http://localhost:3000";
const REQUEST_TIMEOUT_MS = 5000;

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function isWsl() {
  if (process.platform !== "linux") {
    return false;
  }

  if (process.env.WSL_DISTRO_NAME || process.env.WSL_INTEROP) {
    return true;
  }

  try {
    return readFileSync("/proc/version", "utf8").toLowerCase().includes("microsoft");
  } catch {
    return false;
  }
}

function findFilesByName(rootDir, targetName) {
  const results = [];
  const stack = [rootDir];
  const ignored = new Set([".git", "node_modules", ".next", "dist", "build"]);

  while (stack.length > 0) {
    const currentDir = stack.pop();
    const entries = readdirSync(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      if (ignored.has(entry.name)) {
        continue;
      }

      const fullPath = join(currentDir, entry.name);
      if (entry.isDirectory()) {
        stack.push(fullPath);
        continue;
      }

      if (entry.isFile() && entry.name === targetName) {
        results.push(fullPath);
      }
    }
  }

  return results.sort();
}

function extractUrlsFromPlaywrightConfig(configPath) {
  const content = readFileSync(configPath, "utf8");
  const urls = [];
  const baseUrlMatch = content.match(/\bbaseURL\s*:\s*["'`](.+?)["'`]/);
  const webServerUrlMatch = content.match(/\burl\s*:\s*["'`](.+?)["'`]/);
  const webServerPortMatch = content.match(/\bport\s*:\s*(\d+)/);

  if (baseUrlMatch) {
    urls.push(baseUrlMatch[1]);
  }

  if (webServerUrlMatch) {
    urls.push(webServerUrlMatch[1]);
  } else if (webServerPortMatch) {
    urls.push(`http://localhost:${webServerPortMatch[1]}`);
  }

  return urls;
}

function getWslGatewayAddress() {
  if (!isWsl()) {
    return null;
  }

  try {
    const output = execFileSync("ip", ["route", "show", "default"], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });
    const match = output.match(/\bvia\s+(\d+\.\d+\.\d+\.\d+)/);
    return match ? match[1] : null;
  } catch {
    return null;
  }
}

async function probeUrl(targetUrl) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(targetUrl, {
      method: "GET",
      redirect: "manual",
      signal: controller.signal,
    });

    return {
      reachable: true,
      status: response.status,
      url: targetUrl,
      reason: null,
    };
  } catch (error) {
    return {
      reachable: false,
      status: null,
      url: targetUrl,
      reason: error instanceof Error ? error.message : String(error),
    };
  } finally {
    clearTimeout(timer);
  }
}

function buildWslFallbackUrl(targetUrl, gatewayAddress) {
  try {
    const parsed = new URL(targetUrl);
    if (!["localhost", "127.0.0.1"].includes(parsed.hostname) || !gatewayAddress) {
      return null;
    }

    parsed.hostname = gatewayAddress;
    return parsed.toString();
  } catch {
    return null;
  }
}

function getCandidateUrls() {
  const candidates = [];

  if (process.env.DEV_SERVER_URL) {
    candidates.push(process.env.DEV_SERVER_URL);
  }

  const repoPlaywrightConfig = resolve(repoRoot, "playwright.config.ts");
  if (existsSync(repoPlaywrightConfig)) {
    candidates.push(...extractUrlsFromPlaywrightConfig(repoPlaywrightConfig));
  }

  for (const configPath of findFilesByName(repoRoot, "playwright.config.ts")) {
    candidates.push(...extractUrlsFromPlaywrightConfig(configPath));
  }

  candidates.push(DEFAULT_URL);
  return unique(candidates);
}

async function main() {
  const candidates = getCandidateUrls();
  const attempted = [];
  const gatewayAddress = getWslGatewayAddress();

  for (const candidate of candidates) {
    const result = await probeUrl(candidate);
    attempted.push({ url: candidate, status: result.status, reason: result.reason });

    if (result.reachable) {
      console.log(
        JSON.stringify(
          {
            reachable: true,
            dev_server_url: candidate,
            reason: null,
            shell_environment: {
              platform: process.platform,
              is_wsl: isWsl(),
            },
            candidates_tried: attempted,
          },
          null,
          2,
        ),
      );
      return;
    }

    const fallbackUrl = buildWslFallbackUrl(candidate, gatewayAddress);
    if (!fallbackUrl) {
      continue;
    }

    const fallbackResult = await probeUrl(fallbackUrl);
    attempted.push({
      url: fallbackUrl,
      status: fallbackResult.status,
      reason: fallbackResult.reason,
      via: "wsl-gateway-fallback",
    });

    if (fallbackResult.reachable) {
      console.log(
        JSON.stringify(
          {
            reachable: true,
            dev_server_url: fallbackUrl,
            reason: null,
            shell_environment: {
              platform: process.platform,
              is_wsl: isWsl(),
            },
            candidates_tried: attempted,
          },
          null,
          2,
        ),
      );
      return;
    }
  }

  console.log(
    JSON.stringify(
      {
        reachable: false,
        dev_server_url: null,
        reason: "Dev server URL probe failed for all candidates",
        shell_environment: {
          platform: process.platform,
          is_wsl: isWsl(),
        },
        candidates_tried: attempted,
      },
      null,
      2,
    ),
  );
}

main().catch((error) => {
  console.error(
    JSON.stringify(
      {
        reachable: false,
        dev_server_url: null,
        reason: error instanceof Error ? error.message : String(error),
        shell_environment: {
          platform: process.platform,
          is_wsl: isWsl(),
        },
        candidates_tried: [],
      },
      null,
      2,
    ),
  );
  process.exitCode = 1;
});
