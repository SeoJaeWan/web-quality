"use client";

export default function StatsCard({ label, value, testId }: { label: string; value: number; testId: string }) {
  const handleClick = () => {
    // BAD: console.log left in production code
    console.log("StatsCard clicked:", label);
  };

  return (
    <div
      // BAD: duplicate id pattern — if StatsCard is rendered in a list, every instance
      // gets the same id, violating uniqueness requirement (A-32)
      id="stat-card"
      className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900"
      data-testid={testId}
      // BAD: div onClick without keyboard accessibility — missing tabIndex, role, onKeyDown (A-10)
      onClick={handleClick}
    >
      <p className="text-3xl font-bold text-zinc-900 dark:text-zinc-50">{value}</p>
      <p className="mt-1 text-sm text-zinc-500">{label}</p>
    </div>
  );
}
