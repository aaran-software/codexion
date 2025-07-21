"use client";

import {
  ChevronsUpDown,
  UserCircle2,
  UserLock,
  CircleHelp,
  LogOut,
  ChevronRightIcon,
} from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "../avatar";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../dropdown-menu";

import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "./sidebar";

import { useNavigate } from "react-router-dom";
import HelpMenu from "./HelpMenu";
import { useRef, useState } from "react";
// import { useAuth } from "../../pages/auth/AuthContext";
import { useAppContext } from "../../pages/GlobalContext/AppContaxt";
import { logoutUser } from "../../pages/app/auth/logout";

export function NavUser({
  user,
}: {
  user: {
    name: string;
    email: string;
    avatar: string;
  };
}) {
  const { isMobile } = useSidebar();
  const navigate = useNavigate();
  const [showHelpMenu, setShowHelpMenu] = useState(false);
  // const { logout } = useAuth();
  const { API_URL } = useAppContext();
   const handleLogout = () => {
    logoutUser(API_URL);
    // logout();
    navigate("/");
  };
  const helpTimeout = useRef<NodeJS.Timeout | null>(null);
  return (
    <SidebarMenu className="relative">
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <Avatar className="h-8 w-8 rounded-lg">
                <AvatarImage src={user.avatar} alt={user.name} />
                <AvatarFallback className="rounded-lg bg-foreground/20">
                  CN
                </AvatarFallback>
              </Avatar>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-medium">{user.name}</span>
                <span className="truncate text-xs">{user.email}</span>
              </div>
              <ChevronsUpDown className="ml-auto size-4" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>

          <DropdownMenuContent
            className="min-w-56 rounded-lg bg-background text-foreground"
            side={isMobile ? "bottom" : "right"}
            align="end"
            sideOffset={4}
          >
            <DropdownMenuLabel className="p-0 font-normal">
              <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                <Avatar className="h-8 w-8 rounded-lg">
                  <AvatarImage src={user.avatar} alt={user.name} />
                  <AvatarFallback className="rounded-lg">CN</AvatarFallback>
                </Avatar>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-medium">{user.name}</span>
                  <span className="truncate text-xs">{user.email}</span>
                </div>
              </div>
            </DropdownMenuLabel>

            <DropdownMenuSeparator />

            <DropdownMenuGroup>
              <DropdownMenuItem>
                <UserCircle2 />
                Your account
              </DropdownMenuItem>
              <DropdownMenuItem>
                <UserLock />
                Change password
              </DropdownMenuItem>
            </DropdownMenuGroup>

            <DropdownMenuSeparator />

            <DropdownMenuGroup
              onMouseEnter={() => {
                if (helpTimeout.current) clearTimeout(helpTimeout.current);
                setShowHelpMenu(true);
              }}
              onMouseLeave={() => {
                helpTimeout.current = setTimeout(() => {
                  setShowHelpMenu(false);
                }, 150); // small delay to allow hover into HelpMenu
              }}
            >
              <button
                type="button"
                onClick={() => {
                  setShowHelpMenu(true);
                }}
                className="flex items-center w-full text-sm px-2 py-2 text-left hover:bg-muted rounded-sm cursor-pointer"
              >
                <CircleHelp className="w-4 mr-2 text-foreground/70" />
                Help
                <ChevronRightIcon className="block ml-auto" />
              </button>

              {showHelpMenu && (
                <div
                  onMouseEnter={() => {
                    if (helpTimeout.current) clearTimeout(helpTimeout.current);
                    setShowHelpMenu(true);
                  }}
                  onMouseLeave={() => {
                    helpTimeout.current = setTimeout(() => {
                      setShowHelpMenu(false);
                    }, 150);
                  }}
                  className="absolute bottom-0 z-50 left-0 sm:left-full"
                >
                  <HelpMenu onClose={() => setShowHelpMenu(false)} />
                </div>
              )}
            </DropdownMenuGroup>
            <DropdownMenuSeparator />

            <DropdownMenuItem className="text-delete" onClick={handleLogout}>
              <LogOut className="text-delete" />
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
