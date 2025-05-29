"use client"

import { Avatar } from "./ui/avatar"
import { Menu } from "./ui/menu"
import {
  IconDashboard,
  IconLogout,
  IconMoon,
  IconSettings,
  IconSun,
} from "@intentui/icons"
import { useTheme } from "next-themes"
import { signIn, useSession } from "next-auth/react"
import { useEffect, useState } from "react" // Added useEffect and useState

export function HeaderMenu() {
  const { resolvedTheme, setTheme } = useTheme()
  const { data: session } = useSession()
  const [isAdmin, setIsAdmin] = useState(false)

  useEffect(() => {
    const checkAdminStatus = async () => {
      if (session) {
        try {
          const response = await fetch('/api/auth/is-admin');
          if (response.ok) {
            const data = await response.json();
            setIsAdmin(data.isAdmin);
          } else {
            console.error("Failed to fetch admin status:", response.status);
            setIsAdmin(false); // Default to false on error
          }
        } catch (error) {
          console.error("Error fetching admin status:", error);
          setIsAdmin(false); // Default to false on error
        }
      } else {
        setIsAdmin(false); // Not logged in, not an admin
      }
    };

    checkAdminStatus();
  }, [session]);
  
  if (!session) {
    return (
      <Menu>
        <Menu.Trigger aria-label="Open Menu">
          <Avatar 
            alt="Guest" 
            size="extra-large" 
            src="/icon.jpg"
          />
        </Menu.Trigger>
        <Menu.Content placement="bottom" showArrow className="sm:min-w-64">
          <Menu.Header separator>
            <span className="block">Guest</span>
            <span className="font-normal text-muted-fg">Not signed in</span>
          </Menu.Header>

          <Menu.Submenu>
            <Menu.Item>
              {resolvedTheme === "light" ? (
                <IconSun />
              ) : (
                <IconMoon />
              )}
              <Menu.Label>Switch Theme</Menu.Label>
            </Menu.Item>
            <Menu.Content>
              <Menu.Item onAction={() => setTheme("dark")}>
                <IconMoon /> Dark
              </Menu.Item>
              <Menu.Item onAction={() => setTheme("light")}>
                <IconSun /> Light
              </Menu.Item>
            </Menu.Content>
          </Menu.Submenu>
          <Menu.Separator />
          <Menu.Item onAction={() => signIn("google")}>
            <span className="menu-label">Sign In / Register</span>
          </Menu.Item>
        </Menu.Content>
      </Menu>
    )
  }

  return (
    <Menu>
      <Menu.Trigger aria-label="Open Menu">
        <Avatar 
          alt={session?.user?.name || "User"} 
          size="extra-large" 
          src={session?.user?.image || undefined} 
        />
      </Menu.Trigger>
      <Menu.Content placement="bottom" showArrow className="sm:min-w-64">
        <Menu.Header separator>
          <span className="block">{session?.user?.name || "User"}</span>
          <span className="font-normal text-muted-fg">{session?.user?.email || ""}</span>
        </Menu.Header>

        <Menu.Section>
          <Menu.Item href="#dashboard">
            <IconDashboard />
            <Menu.Label>My Quests</Menu.Label>
          </Menu.Item>
          <Menu.Item href="/submit-challenge">
            {/* Add an appropriate icon if available, e.g. IconPlus or IconUpload */}
            <Menu.Label>Submit Questions</Menu.Label> 
          </Menu.Item>
          {isAdmin && (
            <Menu.Item href="/admin/challenges">
              {/* Add an appropriate icon if available, e.g., IconShieldLock or IconSettingsCog */}
              <Menu.Label>Admin Panel</Menu.Label>
            </Menu.Item>
          )}
          <Menu.Item href="#settings">
            <IconSettings />
            <Menu.Label>Profile</Menu.Label>
          </Menu.Item>
        </Menu.Section>
        <Menu.Separator />
        <Menu.Submenu>
          <Menu.Item>
            {resolvedTheme === "light" ? (
              <IconSun />
            ) : (
              <IconMoon />
            )}
            <Menu.Label>Switch Theme</Menu.Label>
          </Menu.Item>
          <Menu.Content>
            <Menu.Item onAction={() => setTheme("dark")}>
              <IconMoon /> Dark
            </Menu.Item>
            <Menu.Item onAction={() => setTheme("light")}>
              <IconSun /> Light
            </Menu.Item>
          </Menu.Content>
        </Menu.Submenu>
        <Menu.Item href="#contact-s">
          <Menu.Label>Contact Support</Menu.Label>
        </Menu.Item>
        <Menu.Separator />
        <Menu.Item href="#logout">
          <IconLogout />
          <Menu.Label>Log out</Menu.Label>
        </Menu.Item>
      </Menu.Content>
    </Menu>
  )
}
