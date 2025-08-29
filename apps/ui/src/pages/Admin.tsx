import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "../../../../resources/components/breadcrumb";
import { Separator } from "../../../../resources/components/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "../../../../resources/components/sidebar/sidebar";
import { useEffect, useState } from "react";
import { useAppContext } from "../../../global/AppContaxt";
import { useNavigate, useParams } from "react-router-dom";
import { useFrappeAuth } from "../../../global/auth/frappeAuthContext";
import Dashboard from "../../../../resources/components/dashboard/Dashboard";
import AppHeader from "../../../../resources/UIBlocks/header/AppHeader";
import { AppSidebar } from "../../../../resources/components/sidebar/app-sidebar";
import ScrollToTopButton from "../../../../resources/components/common/scrolltotopbutton";
import ButtonComponent from "./ComponentUsage/ButtonComponent";
import AlertComponent from "./ComponentUsage/AlertComponent";
import AccordionComponent from "./ComponentUsage/AccordionComponent";
import CalendarComponent from "./ComponentUsage/CalendarComponent";
import CardComponent from "./ComponentUsage/CardComponent";
import CarouselComponent from "./ComponentUsage/CarouselComponent";
import RadioGroupComponent from "./ComponentUsage/RadioGroupComponent";
import PasswordComponent from "./ComponentUsage/PasswordComponent";
import TextAreaComponent from "./ComponentUsage/TextAreaComponent";
import TextInputComponent from "./ComponentUsage/TextInputComponent";
import FileInputComponent from "./ComponentUsage/FileInputComponent";
import TimelineComponent from "./ComponentUsage/TimeLineComponents";
import ChartComponent from "./ComponentUsage/ChartComponent";
import PinInputComponent from "./ComponentUsage/PinInputComponent";
import ToolTipComponent from "./ComponentUsage/ToolTipComponent";
import StarRatingComponent from "./ComponentUsage/StarRatingComponent";
import NotificationComponent from "./ComponentUsage/NotificationComponent";
import DrawerComponent from "./ComponentUsage/DrawerComponent";
import EditableTableComponent from "./ComponentUsage/EditableTableComponent";
import PrintComponent from "./LayoutUsage/PrintComponent";
import BarCodeComponent from "./ComponentUsage/BarCodeComponent";
import BannerBlock from "./UIBlocksUsage/BannerBlock";
import CardBlock from "./UIBlocksUsage/CardBlock";
import CarouselBlock from "./UIBlocksUsage/CarouselBlock";
import ConsultantBlock from "./UIBlocksUsage/ConsultantBlock";
import ContactBlock from "./UIBlocksUsage/ContactBlock";
import FilterBlock from "./UIBlocksUsage/FilterBlock";
import FooterBlock from "./UIBlocksUsage/FooterBlock";
import HeaderBlock from "./UIBlocksUsage/HeaderBlock";
import ProductBlock from "./UIBlocksUsage/ProductBlock";
import PriceBlock from "./UIBlocksUsage/PriceBlock";
import ProcessBlock from "./UIBlocksUsage/ProcessBlock";
import PromotionBlock from "./UIBlocksUsage/PromotionBlock";
import SliderBlock from "./UIBlocksUsage/SliderBlock";
import StartingBlock from "./UIBlocksUsage/StartingBlock";
import TestimonialBlock from "./UIBlocksUsage/TestimonialBlock";
import MapBlock from "./UIBlocksUsage/MapBlock";
import DocsIntro from "./DocsIntro";
import RatingBlock from "./UIBlocksUsage/RatingBlock";

export default function Admin() {
  const { user } = useFrappeAuth();
  const navigate = useNavigate();
  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user]);

  const { component } = useParams();
  const { currentComponent, setCurrentComponent } = useAppContext();

  // On mount or when URL changes
  useEffect(() => {
    if (component === undefined) {
      setCurrentComponent("dashboard");
    } else if (component !== currentComponent) {
      setCurrentComponent(component);
    }
  }, [component]);

  // Update browser tab title
  useEffect(() => {
    if (currentComponent) {
      const titleMap: Record<string, string> = {
        barcode: "Bar Code",
        dashboard: "Dashboard",
        accordion: "Accordion",
        alert: "Alert",
        button: "Button",
        calendar: "Calendar",
        chart: "Chart",
        card: "Card",
        carousel: "Carousel",
        checkbox: "Checkbox",
        combobox: "Combobox",
        Drawer: "Drawer",
        editabletable: "Editable Table",
        fileinput: "File Input",
        table: "Table",
        textinput: "Text Input",
        timeline: "Timeline",
        textarea: "TextArea",
        texteditor: "Text Editor",
        tooltip: "Tool Tip",
        notification: "Notification",
        password: "Password",
        print: "Print",
        pininput: "Pin Input",
        radiogroup: "Radio Group",
        starrating: "Star Rating",
      };
      document.title = titleMap[currentComponent];
    }
  }, [currentComponent]);

  const [compoent] = useState([
    // Main Content
    {
      id: "dashboard",
      className: "w-[100%] min-h-full",
      component: <DocsIntro />,
    },

    // Components
    {
      id: "accordion",
      className: "flex justify-center p-4",
      component: <AccordionComponent />,
    },
    {
      id: "alert",
      className: "flex justify-center items-center min-h-full",
      component: <AlertComponent />,
    },
    {
      id: "barcode",
      className: "",
      component: <BarCodeComponent />,
    },
    {
      id: "button",
      className: "flex justify-center items-center min-h-full",
      component: <ButtonComponent />,
    },
    {
      id: "calendar",
      className: "flex justify-center items-center min-h-full",
      component: <CalendarComponent />,
    },
    {
      id: "card",
      className: "flex justify-center items-center min-h-full",
      component: <CardComponent />,
    },
    {
      id: "chart",
      className: "flex justify-center items-center min-h-full p-4",
      component: <ChartComponent />,
    },
    {
      id: "carousel",
      className: "flex justify-center items-center min-h-full p-4",
      component: <CarouselComponent />,
    },
    {
      id: "drawer",
      className: "flex justify-center items-center min-h-full p-4",
      component: <DrawerComponent />,
    },
    {
      id: "editabletable",
      className: "flex w-full p-4",
      component: <EditableTableComponent />,
    },
    {
      id: "fileinput",
      className: "flex justify-center items-center min-h-full p-4",
      component: <FileInputComponent />,
    },
    {
      id: "textinput",
      className: "flex justify-center items-center min-h-full p-4",
      component: <TextInputComponent />,
    },
    {
      id: "textarea",
      className: "flex  justify-center items-center min-h-full p-4",
      component: <TextAreaComponent />,
    },
    {
      id: "timeline",
      className: "flex justify-center items-center min-h-full p-4",
      component: <TimelineComponent />,
    },
    {
      id: "tooltip",
      className: "flex justify-center items-center min-h-full p-4",
      component: <ToolTipComponent />,
    },
    {
      id: "notification",
      className: "flex  justify-center items-center min-h-full p-4",
      component: <NotificationComponent />,
    },

    {
      id: "password",
      className: "flex justify-center items-center min-h-full p-4",
      component: <PasswordComponent />,
    },
    {
      id: "pininput",
      className: "flex justify-center items-center min-h-full p-4",
      component: <PinInputComponent />,
    },
    {
      id: "print",
      className: "flex w-full p-4",
      component: <PrintComponent />,
    },
    {
      id: "radiogroup",
      className: "flex justify-center items-center min-h-full p-4",
      component: <RadioGroupComponent />,
    },
    {
      id: "starrating",
      className: "flex justify-center items-center min-h-full p-4",
      component: <StarRatingComponent />,
    },

    //blocks
    {
      id: "bannerblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <BannerBlock />,
    },
    {
      id: "cardblock",
      className: "px-[10%] w-full",
      component: <CardBlock />,
    },
    {
      id: "carouselblock",
      className: "px-[10%]",
      component: <CarouselBlock />,
    },
    {
      id: "consultantblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <ConsultantBlock />,
    },
    {
      id: "contactblock",
      className: "p-4",
      component: <ContactBlock />,
    },
    {
      id: "filterblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <FilterBlock />,
    },
    {
      id: "footerblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <FooterBlock />,
    },
    {
      id: "headerblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <HeaderBlock />,
    },
    {
      id: "productblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <ProductBlock />,
    },
    {
      id: "priceblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <PriceBlock />,
    },
    {
      id: "processblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <ProcessBlock />,
    },
    {
      id: "promotionblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <PromotionBlock />,
    },
    {
      id: "sliderblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <SliderBlock />,
    },
    {
      id: "startingblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <StartingBlock />,
    },
    {
      id: "testimonialblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <TestimonialBlock />,
    },
    {
      id: "mapblock",
      className: "flex justify-center items-center min-h-full p-4",
      component: <MapBlock />,
    },
    {
      id: "rating",
      className: "flex justify-center items-center min-h-full p-4",
      component: <RatingBlock />,
    },
  ]);

  return (
    <SidebarProvider className="flex flex-col min-h-screen bg-dashboard-background text-dashboard-foreground">
      {/* Sticky Docs header */}
      <div className="sticky top-0 z-50 bg-background">
        <AppHeader />
      </div>

      <div className="flex flex-1 min-h-0">
        {/* sidebar */}
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
                  <BreadcrumbItem className="block cursor-pointer">
                    <BreadcrumbLink
                      onClick={() => setCurrentComponent("dashboard")}
                    >
                      Dashboard
                    </BreadcrumbLink>
                  </BreadcrumbItem>
                  <BreadcrumbSeparator className="block" />
                  <BreadcrumbItem className="block">
                    <BreadcrumbPage className="capitalize cursor-pointer">
                      {currentComponent === "dashboard" ? "" : currentComponent}
                    </BreadcrumbPage>
                  </BreadcrumbItem>
                </BreadcrumbList>
              </Breadcrumb>
            </div>
          </header>

          {/* Scrollable Main Area */}
          <main className="flex-1 overflow-auto">
            {component === undefined ? (
              // Render default component (dashboard)
              <div className="w-full min-h-full">
                <DocsIntro />
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
