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
import CustomizeTheme from "./AdminComponents/CustomizeTheme";
import CustomizeLogo from "./AdminComponents/CustomizeLogo";
import Purchase from "./Forms/Invoice/Purchase";
import Sales from "./Forms/Invoice/Sales";
import Payment from "./Forms/Invoice/Payment";
import Receipt from "./Forms/Invoice/Receipt";
import AccountBooks from "./Forms/Transaction/Account-Books";
import AccountHeads from "./Forms/Books/Account-Heads";
import Ledger from "./Forms/Books/Ledger";
import Contacts from "./Forms/Master/Contacts";
import Products from "./Forms/Master/Products";
import Orders from "./Forms/Master/Orders";
import Styles from "./Forms/Master/Styles";
import City from "./Forms/Common/City";
import States from "./Forms/Common/State";
import PinCode from "./Forms/Common/Pin-Codes";
import Countries from "./Forms/Common/Countries";
import HSNCode from "./Forms/Common/HSN-Codes";
import Units from "./Forms/Common/Units";
import Categories from "./Forms/Common/Categories";
import Colours from "./Forms/Common/Colours";
import Size from "./Forms/Common/Sizes";
import Departments from "./Forms/Common/Departments";
import Bank from "./Forms/Common/Bank";
import ReceiptType from "./Forms/Common/Receipt-Type";
import Despatches from "./Forms/Common/Despatches";
import GstPercent from "./Forms/Common/Gst-Percents";
import ContactType from "./Forms/Common/Contact-Types";
import PaymentMode from "./Forms/Common/Payment.Mode";
import { useAuth } from "../auth/AuthContext";
import Dashboard from "../../../Components/Dashboard/Dashboard";
import AppHeader from "../../../Components/Header/AppHeader";
import { AppSidebar } from "../../../Components/Sidebar/app-sidebar";
import ScrollToTopButton from "../../../Components/common/scrolltotop";
import Docker from "../cortex/Docker";
import GrandStream from "./Forms/GrandStream";

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
        themes: "Theme",
        admin: "Dashboard",
        logo: "Customize Logo",
        sales: "Sales",
        purchase: "Purchase",
        receipt: "Receipt",
        payment: "Payment",
        accountbook: "Account Books",
        docker: "Docker",
      };
      document.title = titleMap[currentComponent];
    }
  }, [currentComponent]);

  const [compoent] = useState([
    // Main Content
    {
      id: "themes",
      className: "w-[100%] min-h-full",
      component: <CustomizeTheme />,
    },

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
     {
      id: "calllog",
      className: "w-[100%] min-h-full",
      component: <GrandStream />,
    },
    {
      id: "logo",
      className: "w-[100%] min-h-full",
      component: <CustomizeLogo />,
    },
    {
      id: "purchase",
      className: "w-[100%] min-h-full",
      component: <Purchase />,
    },
    {
      id: "sales",
      className: "w-[100%] min-h-full",
      component: <Sales />,
    },
    {
      id: "receipt",
      className: "w-[100%] min-h-full",
      component: <Receipt />,
    },
    {
      id: "payment",
      className: "w-[100%] min-h-full",
      component: <Payment />,
    },

    // transaction
    {
      id: "accountbook",
      className: "w-[100%] min-h-full",
      component: <AccountBooks />,
    },

    // books
    {
      id: "accounthead",
      className: "w-[100%] min-h-full",
      component: <AccountHeads />,
    },
    {
      id: "ledgergroup",
      className: "w-[100%] min-h-full",
      component: <AccountHeads />,
    },
    {
      id: "ledger",
      className: "w-[100%] min-h-full",
      component: <Ledger />,
    },

    {
      id: "contacts",
      className: "w-[100%] min-h-full",
      component: <Contacts />,
    },
    {
      id: "products",
      className: "w-[100%] min-h-full",
      component: <Products />,
    },
    {
      id: "company",
      className: "w-[100%] min-h-full",
      component: <Ledger />,
    },
    {
      id: "orders",
      className: "w-[100%] min-h-full",
      component: <Orders />,
    },
    {
      id: "styles",
      className: "w-[100%] min-h-full",
      component: <Styles />,
    },

    // common

     {
      id: "city",
      className: "w-[100%] min-h-full",
      component: <City />,
    },
      {
      id: "state",
      className: "w-[100%] min-h-full",
      component: <States />,
    },
      {
      id: "pincode",
      className: "w-[100%] min-h-full",
      component: <PinCode />,
    },
      {
      id: "country",
      className: "w-[100%] min-h-full",
      component: <Countries />,
    },
      {
      id: "hsncode",
      className: "w-[100%] min-h-full",
      component: <HSNCode />,
    },
      {
      id: "units",
      className: "w-[100%] min-h-full",
      component: <Units />,
    },
      {
      id: "category",
      className: "w-[100%] min-h-full",
      component: <Categories />,
    },
      {
      id: "colours",
      className: "w-[100%] min-h-full",
      component: <Colours />,
    },
      {
      id: "sizes",
      className: "w-[100%] min-h-full",
      component: <Size />,
    },
      {
      id: "departments",
      className: "w-[100%] min-h-full",
      component: <Departments />,
    },
      {
      id: "bank",
      className: "w-[100%] min-h-full",
      component: <Bank />,
    },
      {
      id: "receipttype",
      className: "w-[100%] min-h-full",
      component: <ReceiptType />,
    },
      {
      id: "despatches",
      className: "w-[100%] min-h-full",
      component: <Despatches />,
    },
      {
      id: "gstpercent",
      className: "w-[100%] min-h-full",
      component: <GstPercent />,
    },
      {
      id: "contacttype",
      className: "w-[100%] min-h-full",
      component: <ContactType />,
    },
      {
      id: "paymentmode",
      className: "w-[100%] min-h-full",
      component: <PaymentMode />,
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
