import React, { useRef, useState, useEffect } from "react";
import ImageButton from "../../resources/components/button/ImageBtn";

type Point = { x: number; y: number };
type Stroke = {
  points: Point[];
  color: string;
  size: number;
  type: "draw" | "erase";
};

const DrawingCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [strokes, setStrokes] = useState<Stroke[]>([]);
  const [redoStack, setRedoStack] = useState<Stroke[]>([]);
  const [currentStroke, setCurrentStroke] = useState<Stroke | null>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [color, setColor] = useState("#000000");
  const [brushSize, setBrushSize] = useState(5);
  const [mode, setMode] = useState<"draw" | "erase">("draw");

  useEffect(() => {
    redraw();
  }, [strokes]);

  const getCanvasContext = (): CanvasRenderingContext2D | null => {
    const canvas = canvasRef.current;
    return canvas ? canvas.getContext("2d") : null;
  };

  const redraw = () => {
    const ctx = getCanvasContext();
    const canvas = canvasRef.current;
    if (!ctx || !canvas) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const stroke of strokes) {
      ctx.beginPath();
      ctx.lineJoin = "round";
      ctx.lineCap = "round";
      ctx.strokeStyle = stroke.type === "erase" ? "white" : stroke.color;
      ctx.lineWidth = stroke.size;
      stroke.points.forEach((point, index) => {
        if (index === 0) ctx.moveTo(point.x, point.y);
        else ctx.lineTo(point.x, point.y);
      });
      ctx.stroke();
    }
  };

  const startDrawing = (e: React.MouseEvent) => {
    const { offsetX, offsetY } = e.nativeEvent;
    const newStroke: Stroke = {
      points: [{ x: offsetX, y: offsetY }],
      color,
      size: brushSize,
      type: mode,
    };
    setCurrentStroke(newStroke);
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent) => {
    const { offsetX, offsetY } = e.nativeEvent;
    const pos = { x: offsetX, y: offsetY };

    if (!isDrawing) return;

    if (mode === "erase") {
      const newStrokes = strokes.filter((stroke) => {
        return !stroke.points.some((pt) => {
          const dx = pt.x - pos.x;
          const dy = pt.y - pos.y;
          return Math.sqrt(dx * dx + dy * dy) < brushSize * 1.2; // Increased radius
        });
      });

      if (newStrokes.length !== strokes.length) {
        setStrokes(newStrokes);
        setRedoStack([]);
      }

      return;
    }

    if (!currentStroke) return;

    const newPoints = [...currentStroke.points, pos];
    const updatedStroke = { ...currentStroke, points: newPoints };
    setCurrentStroke(updatedStroke);
    setStrokes([...strokes.slice(0, -1), updatedStroke]); // Fix duplication
  };

  const endDrawing = () => {
    if (!isDrawing || !currentStroke) return;

    if (mode === "draw") {
      setStrokes([...strokes, currentStroke]);
      setRedoStack([]);
    } else if (mode === "erase") {
      // Erase strokes and record it as an erase stroke
      const erased = strokes.filter((stroke) =>
        stroke.points.some((pt) => {
          const last = currentStroke.points[currentStroke.points.length - 1];
          const dx = pt.x - last.x;
          const dy = pt.y - last.y;
          return Math.sqrt(dx * dx + dy * dy) < brushSize * 1.2;
        })
      );

      if (erased.length > 0) {
        const remaining = strokes.filter((s) => !erased.includes(s));
        setStrokes(remaining);
        setRedoStack([]);
      }
    }

    setCurrentStroke(null);
    setIsDrawing(false);
  };

  const undo = () => {
    if (strokes.length === 0) return;
    const newStrokes = [...strokes];
    const last = newStrokes.pop();
    setStrokes(newStrokes);
    if (last) setRedoStack([...redoStack, last]);
  };

  const redo = () => {
    if (redoStack.length === 0) return;
    const last = redoStack[redoStack.length - 1];
    setRedoStack(redoStack.slice(0, -1));
    setStrokes([...strokes, last]);
  };

  const clearCanvas = () => {
    setStrokes([]);
    setRedoStack([]);
  };

  const saveDrawing = () => {
    const data = JSON.stringify(strokes);
    localStorage.setItem("drawing", data);
    alert("Saved to localStorage!");
  };

  //   const loadDrawing = () => {
  //     const data = localStorage.getItem("drawing");
  //     if (data) {
  //       setStrokes(JSON.parse(data));
  //     }
  //   };

  const getTouchPos = (touch: Touch): Point => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    return {
      x: touch.clientX - rect.left,
      y: touch.clientY - rect.top,
    };
  };

  const handleTouchStart = (e: React.TouchEvent<HTMLCanvasElement>) => {
    if (e.touches.length === 1) {
      e.preventDefault();
      const touch = e.touches[0] as unknown as Touch;
      const pos = getTouchPos(touch);
      const newStroke: Stroke = {
        points: [pos],
        color,
        size: brushSize,
        type: mode,
      };
      setCurrentStroke(newStroke);
      setIsDrawing(true);
    }
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLCanvasElement>) => {
  if (e.touches.length === 1) {
    e.preventDefault();
    const touch = e.touches[0] as unknown as Touch;
    const pos = getTouchPos(touch);

    if (!isDrawing) return;

    if (mode === "erase") {
      const newStrokes = strokes.filter((stroke) => {
        return !stroke.points.some((pt) => {
          const dx = pt.x - pos.x;
          const dy = pt.y - pos.y;
          return Math.sqrt(dx * dx + dy * dy) < brushSize * 1.2;
        });
      });

      if (newStrokes.length !== strokes.length) {
        setStrokes(newStrokes);
        setRedoStack([]);
      }

      return;
    }

    if (!currentStroke) return;

    const newPoints = [...currentStroke.points, pos];
    const updatedStroke = { ...currentStroke, points: newPoints };
    setCurrentStroke(updatedStroke);
    setStrokes([...strokes.slice(0, -1), updatedStroke]);
  }
};


const handleTouchEnd = (e: React.TouchEvent<HTMLCanvasElement>) => {
  if (isDrawing) {
    e.preventDefault();
    endDrawing();
  }
};

useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.ctrlKey && e.key === "z") {
      e.preventDefault();
      undo();
    }
    if (e.ctrlKey && e.key === "y") {
      e.preventDefault();
      redo();
    }
  };

  window.addEventListener("keydown", handleKeyDown);
  return () => window.removeEventListener("keydown", handleKeyDown);
}, [undo, redo]);


  return (
    <div className="h-screen w-screen flex flex-col bg-gray-100">
      {/* Top Control Bar */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 bg-white border rounded-lg shadow-md p-3 flex flex-wrap gap-3 m-5 z-50">
        <label className="flex items-center space-x-2">
          <span>Color:</span>
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
          />
        </label>
        <label className="flex items-center space-x-2">
          <span>Brush Size:</span>
          <input
            type="range"
            min={1}
            max={50}
            value={brushSize}
            onChange={(e) => setBrushSize(Number(e.target.value))}
          />
          <span>{brushSize}</span>
        </label>
        {/* <button
  className={`p-2 rounded-full ${tool === "pointer" ? "bg-black text-white" : "bg-white"}`}
  onClick={() => setTool("pointer")}
>
  Pointer
</button> */}

        <ImageButton
          onClick={() => setMode("draw")}
          className="px-3 py-1 border bg-blue-100 rounded"
          icon={"draw"}
        />
        <ImageButton
          onClick={() => setMode("erase")}
          className="px-3 py-1 border bg-red-100 rounded"
          icon={"erase"}
        />

        <ImageButton
          onClick={undo}
          className="px-3 py-1 border bg-gray-200 rounded"
          icon={"undo"}
        />

        <ImageButton
          onClick={redo}
          className="px-3 py-1 border bg-gray-200 rounded"
          icon={"redo"}
        />

        <ImageButton
          onClick={saveDrawing}
          className="px-3 py-1 border bg-green-200 rounded"
          icon={"save"}
        />

        <ImageButton
          onClick={clearCanvas}
          className="px-3 py-1 border bg-pink-200 rounded"
          icon={"clear"}
        />
      </div>

      {/* Full-screen Canvas Area */}
      <div className="flex-1 m-5  touch-none">
        <canvas
          ref={canvasRef}
          width={window.innerWidth}
          height={window.innerHeight - 80}
          className="w-[100%] h-[95vh] border-t border-gray-300 bg-white cursor-crosshair"
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={endDrawing}
          onMouseLeave={endDrawing}
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        />
      </div>
    </div>
  );
};

export default DrawingCanvas;
