"use client"

import { Avatar } from "./ui/avatar"
import { Menu } from "./ui/menu"
import {
  IconDashboard,
  IconLogout,
  IconSettings,
} from "@intentui/icons"
import { signIn, signOut, useSession } from "next-auth/react"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

export function HeaderMenu() {
  const { data: session } = useSession()
  const router = useRouter()
  const [adminStatus, setAdminStatus] = useState({ isAdmin: false, isRootAdmin: false })

  // Check if user is admin
  useEffect(() => {
    if (session?.user?.id) {
      fetch('/api/admin/check')
        .then(res => res.json())
        .then(data => setAdminStatus(data))
        .catch(() => setAdminStatus({ isAdmin: false, isRootAdmin: false }));
    }
  }, [session]);

  const handleSignOut = () => {
    signOut();
  };

  const handleNavigation = (path: string) => {
    router.push(path);
  };
  
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
          <Menu.Item onAction={() => handleNavigation('#dashboard')}>
            <IconDashboard />
            <Menu.Label>My Quests</Menu.Label>
          </Menu.Item>
          <Menu.Item onAction={() => handleNavigation('/submit-question')}>
            <IconSettings />
            <Menu.Label>Submit Question</Menu.Label>
          </Menu.Item>
          {adminStatus.isAdmin && (
            <Menu.Item onAction={() => handleNavigation('/admin')}>
              <IconSettings />
              <Menu.Label>Admin Panel</Menu.Label>
            </Menu.Item>
          )}
          <Menu.Item onAction={() => handleNavigation('#settings')}>
            <IconSettings />
            <Menu.Label>Profile</Menu.Label>
          </Menu.Item>
        </Menu.Section>
        <Menu.Separator />
        <Menu.Item onAction={() => handleNavigation('#contact-s')}>
          <Menu.Label>Contact Support</Menu.Label>
        </Menu.Item>
        <Menu.Separator />
        <Menu.Item onAction={handleSignOut}>
          <IconLogout />
          <Menu.Label>Log out</Menu.Label>
        </Menu.Item>
      </Menu.Content>
    </Menu>
  )
}
