import {
  useEffect,
  useState,
} from "react";

export default function useResponsive() {
  const [
    width,
    setWidth,
  ] = useState(
    window.innerWidth
  );

  useEffect(() => {
    let timer;

    function handleResize() {
      clearTimeout(timer);

      timer = setTimeout(() => {
        setWidth(
          window.innerWidth
        );
      }, 100);
    }

    window.addEventListener(
      "resize",
      handleResize
    );

    return () => {
      clearTimeout(timer);

      window.removeEventListener(
        "resize",
        handleResize
      );
    };
  }, []);

  return {
    width,
    mobile: width < 768,
    tablet:
      width >= 768 &&
      width < 1100,
    desktop:
      width >= 1100,
  };
}