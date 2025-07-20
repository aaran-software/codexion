import { useEffect, useRef } from "react"
import ImageButton from "../Button/ImageBtn"

export default function HelpMenu({
  onClose,
}: {
  onClose: () => void
}) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        onClose()
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [onClose])

  const options = [
    "Feedback",
    "Keyboard Shortcuts",
    "Markdown Reference",
    "FAQ",
    "Documentation",
    "Video Demos",
    "Service Status",
    "Maintenance Calendar",
    "Support",
    "About YouTrack",
  ]

  return (
    <div
      ref={ref}
      className="sm:ml-2 w-64 bg-background p-2 text-foreground shadow-xl rounded-md z-50"
    >
    <ImageButton className="block ml-auto border border-ring/30 p-1" icon={"close"} onClick={onClose} />

      {options.map((opt, i) => (
        <div
          key={i}
          className="px-4 py-2 text-sm hover:bg-background/20 cursor-pointer"
        >
          {opt}
        </div>
      ))}
      <div className="p-4 text-xs text-foreground/50 border-t border-ring/30">
        Business Management Software<br />
        <span>Build 2025.1.82518<br />Friday, June 20, 2025</span><br />
        <span>Aaran Software</span>
      </div>
    </div>
  )
}
