import {
  PanelSection,
  PanelSectionRow,
  SliderField,
  staticClasses,
  definePlugin,
} from "@decky/ui";
import { callable } from "@decky/api";
import { useState, useEffect } from "react";
import { FaSun } from "react-icons/fa";

const getBrightness = callable<[], number>("get_brightness");
const setBrightness = callable<[percent: number], boolean>("set_brightness");

function Content() {
  const [brightness, setBrightnessState] = useState<number>(50);
  const [loading, setLoading] = useState<boolean>(true);

  const loadBrightness = async () => {
    try {
      const result = await getBrightness();
      if (result >= 0) {
        setBrightnessState(result);
      }
    } catch (e) {
      console.error("Failed to get brightness:", e);
    }
    setLoading(false);
  };

  const handleBrightnessChange = async (value: number) => {
    setBrightnessState(value);
    try {
      await setBrightness(value);
    } catch (e) {
      console.error("Failed to set brightness:", e);
    }
  };

  useEffect(() => {
    loadBrightness();
  }, []);

  return (
    <PanelSection title="Display Brightness">
      <PanelSectionRow>
        {loading ? (
          <div>Loading...</div>
        ) : (
          <SliderField
            label="Brightness"
            value={brightness}
            min={1}
            max={100}
            step={1}
            showValue={true}
            onChange={handleBrightnessChange}
          />
        )}
      </PanelSectionRow>
    </PanelSection>
  );
}

export default definePlugin(() => {
  return {
    title: <div className={staticClasses.Title}>LGO2 Brightness</div>,
    content: <Content />,
    icon: <FaSun />,
  };
});
