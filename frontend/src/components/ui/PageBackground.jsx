import React from 'react';

export function PageBackground() {
    return (
        <div className="fixed inset-0 w-full h-full overflow-hidden pointer-events-none -z-50 bg-slate-50">
            {/* Primary Ambient Gradient */}
            <div className="absolute top-[-20%] right-[-10%] w-[80vw] h-[80vw] bg-indigo-500/20 rounded-full blur-[120px] mix-blend-multiply animate-pulse duration-[8000ms]"></div>

            {/* Secondary Ambient Gradient */}
            <div className="absolute bottom-[-20%] left-[-10%] w-[70vw] h-[70vw] bg-purple-500/20 rounded-full blur-[100px] mix-blend-multiply animate-pulse duration-[10000ms] delay-1000"></div>

            {/* Tertiary - Accent Pop */}
            <div className="absolute top-[40%] left-[30%] w-[40vw] h-[40vw] bg-blue-400/10 rounded-full blur-[80px] mix-blend-multiply animate-pulse duration-[12000ms] delay-2000"></div>

            {/* Noise Texture for Texture/Premium Feel */}
            <div className="absolute inset-0 opacity-[0.4] mix-blend-overlay"
                style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")` }}>
            </div>

            {/* Subtle Grid Pattern Overlay */}
            <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:48px_48px] mask-gradient"></div>
        </div>
    );
}
