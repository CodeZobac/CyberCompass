
import {
  Card as UICard,
  CardContent as UICardContent,
  CardDescription as UICardDescription,
  CardFooter as UICardFooter,
  CardHeader as UICardHeader,
  CardTitle as UICardTitle,
} from "./ui/card"

import { cn } from "@lib/utils"

// Define prop types for all the retro card components
type RetroCardProps = React.ComponentProps<typeof UICard>
type RetroCardHeaderProps = React.ComponentProps<typeof UICardHeader>
type RetroCardTitleProps = React.ComponentProps<typeof UICardTitle>
type RetroCardDescriptionProps = React.ComponentProps<typeof UICardDescription>
type RetroCardContentProps = React.ComponentProps<typeof UICardContent>
type RetroCardFooterProps = React.ComponentProps<typeof UICardFooter>

// Example data for demo purposes
const notifications = [
  {
    title: "Someone subscribe in a New York.",
    description: "1 hour ago",
  },
]

// Reusable RetroCard components with consistent retro styling
export function RetroCard({ className, children, ...props }: RetroCardProps) {
  return (
    <UICard 
      className={cn(
        "w-full max-w-[380px] border-4 border-black transition-all", 
        className
      )} 
      {...props}
    >
      {children}
    </UICard>
  )
}

export function RetroCardHeader({ className, children, ...props }: RetroCardHeaderProps) {
  return (
    <UICardHeader className={cn("", className)} {...props}>
      {children}
    </UICardHeader>
  )
}

export function RetroCardTitle({ className, children, ...props }: RetroCardTitleProps) {
  return (
    <UICardTitle className={cn("text-xl font-bold", className)} {...props}>
      {children}
    </UICardTitle>
  )
}

export function RetroCardDescription({ className, children, ...props }: RetroCardDescriptionProps) {
  return (
    <UICardDescription className={cn("text-sm", className)} {...props}>
      {children}
    </UICardDescription>
  )
}

export function RetroCardContent({ className, children, ...props }: RetroCardContentProps) {
  return (
    <UICardContent className={cn("", className)} {...props}>
      {children}
    </UICardContent>
  )
}

export function RetroCardFooter({ className, children, ...props }: RetroCardFooterProps) {
  return (
    <UICardFooter className={cn("", className)} {...props}>
      {children}
    </UICardFooter>
  )
}

// Demo component to show usage example
export function CardDemo() {
  return (
    <RetroCard>
      <RetroCardHeader>
        <RetroCardTitle>Notifications</RetroCardTitle>
        <RetroCardDescription>You have 3 unread messages.</RetroCardDescription>
      </RetroCardHeader>
      <RetroCardContent className="grid gap-4">
        <div className="w-full flex items-center space-x-4 rounded-sm border border-black border-2 p-4">
          <div className="flex-1 space-y-1">
            <p className="text-sm font-medium leading-none">
              Push Notifications
            </p>
            <p className="text-sm text-muted-foreground">
              Send notifications to device.
            </p>
          </div>
        </div>
        <div>
          {notifications.map((notification, index) => (
            <div
              key={index}
              className="mb-4 grid grid-cols-[25px_1fr] items-start p-4 border-2 border-black transition-all"
            >
              <span className="flex size-2 translate-y-1 rounded-full bg-sky-500" />
              <div className="space-y-1">
                <p className="text-sm font-medium leading-none">
                  {notification.title}
                </p>
                <p className="text-sm text-muted-foreground">
                  {notification.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </RetroCardContent>
      <RetroCardFooter>
      </RetroCardFooter>
    </RetroCard>
  )
}
