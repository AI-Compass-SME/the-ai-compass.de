import React, { useState } from 'react';
import { cn } from "@/lib/utils";

export function ImageWithFallback({ src, alt, className, ...props }) {
    const [imgSrc, setImgSrc] = useState(src);
    const [hasError, setHasError] = useState(false);

    const handleError = () => {
        setHasError(true);
        // Fallback to a placeholder service or asset if needed, currently just logging/handling
        // setImgSrc('/placeholder.jpg'); 
    };

    if (hasError) {
        return (
            <div className={cn("bg-slate-200 flex items-center justify-center text-slate-400", className)} {...props}>
                <span className="text-sm">Image not available</span>
            </div>
        );
    }

    return (
        <img
            src={imgSrc}
            alt={alt}
            className={className}
            onError={handleError}
            {...props}
        />
    );
}
