"use client";

import type { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "ghost" | "danger";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

/** Small, styled button. Variants map to CSS classes in globals.css. */
export function Button({ variant = "primary", className = "", ...rest }: ButtonProps) {
  return <button className={`btn btn--${variant} ${className}`} {...rest} />;
}
