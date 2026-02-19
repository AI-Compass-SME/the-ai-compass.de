import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
    "inline-flex items-center justify-center white-space-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    {
        variants: {
            variant: {
                default: "bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/40 hover:from-indigo-700 hover:to-violet-700 active:scale-[0.98]",
                destructive:
                    "bg-destructive text-destructive-foreground hover:bg-destructive/90 shadow-sm hover:shadow-md",
                outline:
                    "border border-slate-200 bg-white hover:bg-slate-50 hover:text-indigo-600 hover:border-indigo-200 text-slate-700 shadow-sm",
                secondary:
                    "bg-slate-100 text-slate-900 hover:bg-slate-200 shadow-inner",
                ghost: "hover:bg-indigo-50 hover:text-indigo-700",
                link: "text-indigo-600 underline-offset-4 hover:underline",
                premium: "bg-gradient-to-r from-amber-200 to-yellow-400 text-amber-900 shadow-lg shadow-amber-500/20 hover:shadow-amber-500/40 hover:from-amber-300 hover:to-yellow-500 font-bold",
            },
            size: {
                default: "h-10 px-4 py-2",
                sm: "h-9 rounded-md px-3",
                lg: "h-11 rounded-md px-8",
                icon: "h-10 w-10",
            },
        },
        defaultVariants: {
            variant: "default",
            size: "default",
        },
    }
)

const Button = React.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
        <Comp
            className={cn(buttonVariants({ variant, size, className }))}
            ref={ref}
            {...props}
        />
    )
})
Button.displayName = "Button"

export { Button, buttonVariants }
