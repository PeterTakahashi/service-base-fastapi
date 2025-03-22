export type StatusKey =
  | "init"
  | "upload"
  | "pending"
  | "detection"
  | "ocr"
  | "mask-generation"
  | "inpainting"
  | "upscaling"
  | "translating"
  | "rendering"
  | "finished"
  | "error"
  | "error-upload"
  | "error-lang"
  | "error-translating"
  | "error-too-large"
  | "error-disconnect";

export type TranslatorKey = "deepl" | "openai" | "deepseek" | "none";

export const validTranslators: TranslatorKey[] = [
  "deepl",
  "openai",
  "deepseek",
  "none",
];

export type Step = {
  name: string;
  href: string;
  status: "complete" | "current" | "upcoming";
};
