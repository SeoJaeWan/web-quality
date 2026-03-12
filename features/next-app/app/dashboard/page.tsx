"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { useTodos } from "@/contexts/TodoContext";
import StatsCard from "@/components/StatsCard";
import TodoForm from "@/components/TodoForm";
import NotificationList from "@/components/NotificationList";

export default function DashboardPage() {
  const { user, isAuthenticated, mounted } = useAuth();
  const { todos, addTodo } = useTodos();
  const router = useRouter();
  const containerRef = useRef<HTMLDivElement>(null);
  const [recentItems, setRecentItems] = useState<string[]>([]);

  useEffect(() => {
    if (mounted && !isAuthenticated) router.push("/login");
  }, [mounted, isAuthenticated, router]);

  useEffect(() => {
    // BAD: layout thrashing — reads layout property then writes style
    if (containerRef.current) {
      const h = containerRef.current.offsetHeight; // forces reflow
      containerRef.current.style.minHeight = h + "px"; // triggers another reflow
    }

    // BAD: dynamic content insertion without size reservation (CLS risk)
    setTimeout(() => {
      setRecentItems(["프로젝트 회의", "코드 리뷰", "배포 준비"]);
    }, 500);
  }, []);

  if (!mounted || !isAuthenticated) return null;

  const completed = todos.filter((t) => t.completed).length;
  const pending = todos.length - completed;

  return (
    <div>
      <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50" data-testid="greeting">
        안녕하세요, {user?.name}님
      </h1>
      <p className="mt-1 text-sm text-zinc-500">오늘도 좋은 하루 되세요!</p>
      <p className="mt-1 text-xs text-zinc-400" data-testid="current-date">
        {new Date().toLocaleDateString("ko-KR")}
      </p>

      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <StatsCard label="전체 할 일" value={todos.length} testId="stat-total" />
        <StatsCard label="완료" value={completed} testId="stat-completed" />
        <StatsCard label="진행중" value={pending} testId="stat-pending" />
      </div>

      {/* BAD: icon buttons without aria-label */}
      <div className="mt-4 flex gap-2">
        <button data-testid="btn-refresh">
          <svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" /></svg>
        </button>
        <button data-testid="btn-settings">
          <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" /></svg>
        </button>
      </div>

      <div className="mt-8" ref={containerRef}>
        <h2 className="mb-4 text-lg font-semibold text-zinc-900 dark:text-zinc-50">빠른 추가</h2>
        <TodoForm onSubmit={addTodo} />

        {/* BAD: dynamic items without size reservation — CLS */}
        {recentItems.map((item) => (
          <div className="border p-2 mt-2">{item}</div>
        ))}
      </div>

      <div className="mt-8">
        <h2 className="mb-4 text-lg font-semibold text-zinc-900 dark:text-zinc-50">알림</h2>
        <NotificationList />
      </div>

      {/* BAD: image missing alt attribute */}
      <img src="/promo-banner.png" className="mt-6 w-full" />
      {/* BAD: image missing width/height (CLS risk), no loading="lazy" for below-fold */}
      <img src="/footer-ad.png" alt="Advertisement" className="mt-4" />

      <div className="mt-6">
        <Link
          href="/todos"
          className="text-sm text-blue-600 hover:text-blue-800"
          data-testid="go-to-todos"
        >
          전체 할 일 목록 보기 &rarr;
        </Link>
      </div>
    </div>
  );
}
