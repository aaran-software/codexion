import { useState } from "react";

function ProjectManagement() {
  const [projects, setProjects] = useState([
    {
      id: "1",
      title: "Project Aaran",
      description: "A complete admin dashboard for business operations.",
      status: "active", // or "inactive"
      lastBuild: "2025-07-24 10:45 AM",
      fileSize: "12.5 MB",
      managedBy: "Muthu R",
      developedBy: "Dev Team A",
    },
    {
      id: "2",
      title: "Project InvoiceX",
      description: "Handles invoicing and PDF generation for all clients.",
      status: "inactive",
      lastBuild: "2025-07-15 04:22 PM",
      fileSize: "8.3 MB",
      managedBy: "Saran R",
      developedBy: "Dev Team B",
    },
  ]);

  return (
    <div className="grid grid-cols-1 gap-4 p-4">
      {projects.map((project, index) => (
        <div
          key={project.id}
          className="relative bg-white rounded-xl shadow-md border border-gray-200 p-6 flex flex-col justify-between"
        >
          {/* Status Indicator */}
          <div className="absolute top-4 right-4">
            <span
              className={`h-3 w-3 rounded-full inline-block ${
                project.status === "active"
                  ? "bg-green-500 animate-ping duration-[100ms]"
                  : "bg-red-500 animate-ping duration-[100ms]"
              }`}
              title={project.status}
            ></span>
          </div>

          {/* Title & Description */}
          <div>
            <h2 className="text-lg font-semibold text-gray-800">
              {project.title}
            </h2>
            <p className="text-sm text-gray-600 mt-1">{project.description}</p>
          </div>

          {/* Footer Info */}
          <div className="mt-6 grid grid-cols-2 gap-y-2 text-sm text-gray-700">
            <div>
              <span className="font-medium">Last Build:</span> {project.lastBuild}
            </div>
            <div>
              <span className="font-medium">Size:</span> {project.fileSize}
            </div>
            <div>
              <span className="font-medium">Managed By:</span> {project.managedBy}
            </div>
            <div>
              <span className="font-medium">Developed By:</span> {project.developedBy}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ProjectManagement;
