import { Disclosure } from "@headlessui/react";
import React from "react";
import { Icon } from "@iconify/react";

type Props = {};

export const Header: React.FC<Props> = () => {
  return (
    <Disclosure as="nav" className="bg-white shadow">
      <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div className="relative flex h-16 justify-between">
          <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
            <div className="flex shrink-0 items-center text-teal-500">
              <span className="bg-slate-100 p-1 rounded-md">
                <Icon icon="carbon:translate" className="w-8 h-8" />
              </span>
            </div>
            <div className="sm:ml-6 sm:flex sm:space-x-8">
              <a
                href="/"
                className="inline-flex items-center px-1 pt-1 font-medium text-gray-900"
              >
                Baltoon AI Translator
              </a>
            </div>
          </div>
        </div>
      </div>
    </Disclosure>
  );
};
