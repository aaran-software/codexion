import Tooltip from "../../../../../resources/components/tooltip/tooltip"

function ToolTipComponent() {
    return (
        <div>
            <Tooltip content="Hello! I'm a tooltip" side="top" delayDuration={200}>
                <button className="px-3 py-1 rounded bg-blue-600 text-white">
                    Hover me
                </button>
            </Tooltip>

        </div>
    )
}

export default ToolTipComponent