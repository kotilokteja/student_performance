import { Link } from "@tanstack/react-router";
import {
  LayoutGrid,
  ClipboardCheck,
  BarChart3,
  Database,
  BookOpen,
  ShieldCheck,
  type LucideIcon,
} from "lucide-react";
import type { ReactNode } from "react";

const NAV: { group: string; items: { label: string; to: string; icon: LucideIcon }[] }[] = [
  {
    group: "Overview",
    items: [
      { label: "Dashboard", to: "/", icon: LayoutGrid },
      { label: "Risk Assessment", to: "/assessment", icon: ClipboardCheck },
    ],
  },
  {
    group: "Analytics",
    items: [
      { label: "Model Performance", to: "/performance", icon: BarChart3 },
      { label: "Dataset Insights", to: "/insights", icon: Database },
    ],
  },
  {
    group: "Project",
    items: [{ label: "About", to: "/about", icon: BookOpen }],
  },
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background">
      <aside className="sticky top-0 hidden h-screen w-64 shrink-0 flex-col border-r border-sidebar-border bg-sidebar lg:flex">
        <div className="flex items-center gap-3 px-5 py-6">
          <div className="flex size-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <ShieldCheck className="size-5" />
          </div>
          <div>
            <div className="text-sm font-semibold tracking-tight text-sidebar-foreground">Aegis</div>
            <div className="text-xs text-muted-foreground">Academic Early-Warning</div>
          </div>
        </div>

        <nav className="flex-1 space-y-6 px-3 py-2">
          {NAV.map((section) => (
            <div key={section.group}>
              <div className="px-2 pb-2 text-[11px] font-semibold uppercase tracking-widest text-muted-foreground">
                {section.group}
              </div>
              <div className="space-y-1">
                {section.items.map(({ label, to, icon: Icon }) => (
                  <Link
                    key={to}
                    to={to}
                    activeOptions={{ exact: to === "/" }}
                    className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-sidebar-foreground/80 transition-colors hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
                    activeProps={{
                      className:
                        "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground",
                    }}
                  >
                    <Icon className="size-4" />
                    {label}
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </nav>

        <div className="border-t border-sidebar-border px-5 py-4 text-xs leading-relaxed text-muted-foreground">
          Version 4.0
          <br />
          Screening signal for human review.
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <div className="flex items-center gap-2 overflow-x-auto border-b border-border bg-sidebar px-4 py-3 lg:hidden">
          {NAV.flatMap((s) => s.items).map(({ label, to }) => (
            <Link
              key={to}
              to={to}
              activeOptions={{ exact: to === "/" }}
              className="whitespace-nowrap rounded-md border border-border px-3 py-1.5 text-xs font-medium text-foreground/80"
              activeProps={{
                className:
                  "whitespace-nowrap rounded-md px-3 py-1.5 text-xs font-medium bg-primary text-primary-foreground border border-primary",
              }}
            >
              {label}
            </Link>
          ))}
        </div>
        <main className="mx-auto w-full max-w-6xl flex-1 px-5 py-8 sm:px-8">{children}</main>
      </div>
    </div>
  );
}

export function PageHeader({
  eyebrow,
  title,
  subtitle,
}: {
  eyebrow: string;
  title: string;
  subtitle: string;
}) {
  return (
    <header className="mb-8">
      <div className="text-[11px] font-semibold uppercase tracking-widest text-primary">{eyebrow}</div>
      <h1 className="mt-2 text-2xl font-semibold tracking-tight text-foreground sm:text-3xl">{title}</h1>
      <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">{subtitle}</p>
    </header>
  );
}

export function StatCard({
  label,
  value,
  hint,
  tone = "default",
}: {
  label: string;
  value: string;
  hint: string;
  tone?: "default" | "risk" | "safe" | "primary";
}) {
  const toneClass =
    tone === "risk"
      ? "text-risk"
      : tone === "safe"
        ? "text-safe"
        : tone === "primary"
          ? "text-primary"
          : "text-foreground";

  return (
    <div className="flex h-full flex-col justify-between rounded-xl border border-border bg-card p-5 shadow-card transition-shadow hover:shadow-elevated">
      <div className="text-xs font-medium uppercase tracking-wide text-muted-foreground">{label}</div>
      <div className={`mt-3 text-3xl font-semibold tracking-tight tabular-nums ${toneClass}`}>{value}</div>
      <div className="mt-2 text-xs leading-relaxed text-muted-foreground">{hint}</div>
    </div>
  );
}

export function Panel({
  title,
  description,
  children,
  className = "",
}: {
  title: string;
  description?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      className={`flex h-full flex-col rounded-xl border border-border bg-card p-5 shadow-card ${className}`}
    >
      <h2 className="text-sm font-semibold tracking-tight text-foreground">{title}</h2>
      {description ? <p className="mt-1 text-xs text-muted-foreground">{description}</p> : null}
      <div className="mt-4 flex-1">{children}</div>
    </section>
  );
}
