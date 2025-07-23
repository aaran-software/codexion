import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "./tooltip"

interface tooltipcomponentprops{
  label:string;
  tip:string;
  className:string
}

function Tooltipcomp({label ,tip,className}:tooltipcomponentprops) {
  return (
    <Tooltip>
      <TooltipTrigger className={`w-max bg-backgrund text-foreground h-max ${className}`}>{label}</TooltipTrigger>
      <TooltipContent>
        <p className="bg-foreground text-background">{tip}</p>
      </TooltipContent>
    </Tooltip>
  )
}

export default Tooltipcomp


// Usage:
// <TooltipComponent label="Click Me" tip="Login Button" className=""/>
