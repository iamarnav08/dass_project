import { Inter } from "next/font/google";
import { ThemeModeScript, useThemeMode } from "flowbite-react";
import AuthNavbar from "../../components/AuthNavbar";
import "../globals.css";
import { use } from "react";
// import { Main } from "next/document";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="">
      <head>
        <ThemeModeScript />
      </head>
      <body
        className={`${inter.className} flex h-screen flex-col bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-200`}
      >
        <main className="flex flex-1 items-center justify-center">{children}</main>
      </body>
    </html>
  );
}
