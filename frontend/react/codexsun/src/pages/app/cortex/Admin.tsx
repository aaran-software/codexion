import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "../../../Components/breadcrumb";
import { Separator } from "../../../Components/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "../../../Components/Sidebar/sidebar";
import { useEffect, useState } from "react";
import { useAppContext } from "../../GlobalContext/AppContaxt";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import Dashboard from "../../../Components/Dashboard/Dashboard";
import AppHeader from "../../../Components/Header/AppHeader";
import { AppSidebar } from "../../../Components/Sidebar/app-sidebar";
import ScrollToTopButton from "../../../Components/common/scrolltotop";
import Docker from "./Docker";

export default function Admin() {
const { token } = useAuth();
const navigate = useNavigate();
useEffect(() => {
  if (!token) {
    navigate("/");
  }
}, [token]);

  const { component } = useParams();
  const { currentComponent, setCurrentComponent } = useAppContext();

  // On mount or when URL changes
  useEffect(() => {
    if (component === undefined) {
      setCurrentComponent("admin");
    } else if (component !== currentComponent) {
      setCurrentComponent(component);
    }
  }, [component]);

  // Update browser tab title
  useEffect(() => {
    if (currentComponent) {
      const titleMap: Record<string, string> = {
        admin: "Dashboard",
        docker: "Docker",
      };
      document.title = titleMap[currentComponent];
    }
  }, [currentComponent]);

  const [compoent] = useState([

    {
      id: "dashboard",
      className: "w-[100%] min-h-full",
      component: <Dashboard />,
    },
    {
      id: "docker",
      className: "w-[100%] min-h-full",
      component: <Docker />,
    },

  ]);

  return (
    <SidebarProvider className="flex flex-col min-h-screen bg-dashboard-background text-dashboard-foreground">
      {/* Sticky App Header */}
      <div className="sticky top-0 z-50 bg-background">
        <AppHeader />
      </div>

      <div className="flex flex-1 min-h-0">
        {/* Sidebar */}
        <AppSidebar />

        {/* Content Area */}
        <SidebarInset className="flex flex-col flex-1 min-h-0 overflow-hidden bg-dashboard-background text-dashboard-foreground">
          {/* Subheader with Breadcrumb */}
          <header className="flex h-16 ml-2 md:ml-0 shrink-0 items-center justify-between gap-2 mr-5 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
            <div className="flex items-center gap-2">
              <SidebarTrigger className="-ml-1 **:text-foreground" />
              <Separator
                orientation="vertical"
                className="mr-2 bg-foreground text-background data-[orientation=vertical]:h-4"
              />
              <Breadcrumb>
                <BreadcrumbList>
                  <BreadcrumbItem className="block">
                    <BreadcrumbLink onClick={() => setCurrentComponent("")}>
                      Dashboard
                    </BreadcrumbLink>
                  </BreadcrumbItem>
                  <BreadcrumbSeparator className="block" />
                  <BreadcrumbItem className="block">
                    <BreadcrumbPage className="capitalize">
                      {currentComponent === "admin" ? "" : currentComponent}
                    </BreadcrumbPage>
                  </BreadcrumbItem>
                </BreadcrumbList>
              </Breadcrumb>
            </div>
          </header>

          {/* Scrollable Main Area */}
          <main className="flex-1 overflow-auto">
            {component === undefined ? (
              // Render default component (Dashboard)
              <div className="w-full min-h-full">
                <Dashboard />
              </div>
            ) : (
              compoent.map((comp, index) =>
                currentComponent === comp.id ? (
                  <div key={index} className={comp.className}>
                    {comp.component}
                  </div>
                ) : null
              )
            )}
          </main>
        </SidebarInset>
      </div>

      <ScrollToTopButton />
    </SidebarProvider>
  );
}
