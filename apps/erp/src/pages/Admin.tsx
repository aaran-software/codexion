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
import CustomizeTheme from "./AdminComponents/CustomizeTheme";
import CustomizeLogo from "./AdminComponents/CustomizeLogo";
import Purchase from "./Invoice/Purchase";
import Sales from "./Invoice/Sales";
import Payment from "./Invoice/Payment";
import Receipt from "./Invoice/Receipt";
import AccountBooks from "./Transaction/Account-Books";
import AccountHeads from "./Books/Account-Heads";
import Ledger from "./Books/Ledger";
import Contacts from "./Master/Contacts";
import Products from "./Master/Products";
import Orders from "./Master/Orders";
import Styles from "./Master/Styles";
import City from "./Common/City";
import States from "./Common/State";
import PinCode from "./Common/Pin-Codes";
import Countries from "./Common/Countries";
import HSNCode from "./Common/HSN-Codes";
import Units from "./Common/Units";
import Categories from "./Common/Categories";
import Colours from "./Common/Colours";
import Size from "./Common/Sizes";
import Departments from "./Common/Departments";
import Bank from "./Common/Bank";
import ReceiptType from "./Common/Receipt-Type";
import Despatches from "./Common/Despatches";
import GstPercent from "./Common/Gst-Percents";
import ContactType from "./Common/Contact-Types";
import PaymentMode from "./Common/Payment.Mode";
import { useFrappeAuth } from "../../../global/auth/frappeAuthContext";
import Dashboard from "../../../../resources/components/dashboard/Dashboard";
import AppHeader from "../../../../resources/components/header/AppHeader";
import { AppSidebar } from "../../../../resources/components/sidebar/app-sidebar";
import ScrollToTopButton from "../../../../resources/components/common/scrolltotopbutton";
import Task from "./AdminComponents/Task";
import AppFooter from "../../../../resources/components/footer/AppFooter";

export default function Admin() {
  const { user } = useFrappeAuth();
  const navigate = useNavigate();
  useEffect(() => {
    if (!user) {
      navigate("/");
    }
  }, [user]);

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
        task: "Task Manager",
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
      id: "task",
      className: "w-[100%] min-h-full",
      component: <Task />,
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
      {/* Sticky App header */}
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
              // Render default component (dashboard)
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
      <AppFooter />
    </SidebarProvider>
  );
}
