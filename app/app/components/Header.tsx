"use client";

import { HeaderMenu } from "./HeaderMenu";
import { useTheme } from "next-themes";
import Image from "next/image";

const Header = () => {
    const { theme } = useTheme();

    return (
        <header className="bg-bg text-white p-4 shadow-md border-b border-gray-700/30 flex justify-between items-center">
            <div className="flex items-center">
                <Image
                    src="/logo-animated.gif"
                    alt="Cyber Compass"
                    width={100}
                    height={100}
                    className="mr-8 ml-24"
                />
                {theme === "dark" ? (
                    <Image
                        src="/cyber-compass-white.svg"
                        alt="Cyber Compass"
                        width={250}
                        height={125}
                        className=""
                    />
                ) : (
                    <Image
                        src="/cyber-compass-black.svg"
                        alt="Cyber Compass"
                        width={250}
                        height={125}
                        className=""
                    />
                )}
            </div>
            <nav className="px-4 mr-24">
                <HeaderMenu />
            </nav>
        </header>
    );
}; 

export default Header;