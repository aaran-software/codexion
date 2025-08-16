import * as React from "react"

// same tiny cn used locally
function cn(...classes: Array<string | false | null | undefined>) {
  return classes.filter(Boolean).join(" ")
}

export function SidebarMenu({ children }: { children: React.ReactNode }) {
  return <ul className="space-y-1">{children}</ul>
}

export function SidebarMenuItem({ children }: { children: React.ReactNode }) {
  return <li className="list-none">{children}</li>
}

export const SidebarMenuButton = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement>
>(({ className, ...props }, ref) => (
  <button
    ref={ref}
    className={cn(
      "w-full flex items-center justify-between rounded-md px-2 py-1.5 text-sm transition-colors",
      "hover:bg-accent hover:text-accent-foreground focus:outline-none focus:ring-1 focus:ring-ring",
      className
    )}
    {...props}
  />
))
SidebarMenuButton.displayName = "SidebarMenuButton"

export function SidebarMenuSub({ children }: { children: React.ReactNode }) {
  return <ul className="ml-4 space-y-1">{children}</ul>
}

// export function SidebarMenuSubItem({ children }: { children: React.ReactNode }) {
//   return <li className="list-none">{children}</li>
// }
