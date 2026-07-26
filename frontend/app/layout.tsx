import type { Metadata } from "next";
import type { ReactNode } from "react";

import "./globals.css";

export const metadata: Metadata = {
  title: "DevBoard",
  description: "In-house Kanban board for software development.",
};

/** Root layout: wraps every page with the app shell header. */
export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="app-header">
          <a href="/" className="app-header__brand">
            <span className="mono app-header__mark">dev/</span>board
          </a>
          <span className="mono app-header__tag">in-house kanban</span>
        </header>
        <main className="app-main">{children}</main>
      </body>
    </html>
  );
}
