import { Progress } from "@/components/atoms/Progress";
import type { StatusKey, Step } from "@/types";
import { defaultSteps } from "@/config";

import { useState, useMemo, useEffect } from "react";

type Props = {
  status: StatusKey | null;
  error: boolean;
};

export const TranslateProgress: React.FC<Props> = ({ status, error }) => {
  const [steps, setSteps] = useState<Step[]>(defaultSteps);
  useEffect(() => {
    const stepIndex = steps.findIndex((step) => step.name === status);

    steps.forEach((step, index) => {
      if (index < stepIndex) {
        step.status = "complete";
      } else if (index === stepIndex) {
        step.status = "current";
      } else {
        step.status = "upcoming";
      }
    });

    setSteps([...steps]);
  }, [status]);

  return (
    <div className="flex flex-col items-center gap-2 text-center text-gray-700">
      <Progress steps={steps} />
    </div>
  );
};
