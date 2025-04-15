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
import { useSession } from "next-auth/react"

export function HeaderMenu() {
  const { resolvedTheme, setTheme } = useTheme()
  const { data: session } = useSession()
  
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
