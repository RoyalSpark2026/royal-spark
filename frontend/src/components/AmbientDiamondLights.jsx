import { motion } from "framer-motion";
import { useEffect, useState } from "react";

const beams = [
  { top: "10%", left: "-8%", width: "42%", rotate: -14, delay: 0 },
  { top: "24%", right: "-10%", width: "38%", rotate: 18, delay: 1.2 },
  { top: "48%", left: "8%", width: "34%", rotate: -9, delay: 2.4 },
  { top: "72%", right: "6%", width: "30%", rotate: 13, delay: 3.1 },
];

export const AmbientDiamondLights = () => {
  const [pointer, setPointer] = useState({ x: 50, y: 22 });

  useEffect(() => {
    const handleMove = (event) => {
      if (window.innerWidth < 1024) return;
      setPointer({
        x: (event.clientX / window.innerWidth) * 100,
        y: (event.clientY / window.innerHeight) * 100,
      });
    };

    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, []);

  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" data-testid="ambient-diamond-lights">
      <motion.div
        className="absolute inset-x-0 top-0 h-[48rem] opacity-90"
        animate={{
          background: [
            `radial-gradient(circle at ${pointer.x}% ${pointer.y}%, rgba(255,255,255,0.14), transparent 18%), radial-gradient(circle at 78% 18%, rgba(240,215,141,0.12), transparent 20%)`,
            `radial-gradient(circle at ${Math.min(pointer.x + 4, 92)}% ${Math.min(pointer.y + 3, 88)}%, rgba(255,255,255,0.18), transparent 19%), radial-gradient(circle at 74% 20%, rgba(240,215,141,0.14), transparent 21%)`,
          ],
        }}
        transition={{ duration: 5.5, repeat: Infinity, repeatType: "mirror", ease: "easeInOut" }}
      />

      {beams.map((beam, index) => (
        <motion.div
          key={index}
          className="absolute h-[1px] rounded-full bg-[linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,0.95),rgba(240,215,141,0.55),rgba(255,255,255,0))] blur-[0.7px]"
          style={{
            top: beam.top,
            left: beam.left,
            right: beam.right,
            width: beam.width,
            transform: `rotate(${beam.rotate}deg)`,
            opacity: 0.2,
          }}
          animate={{
            opacity: [0.06, 0.22, 0.08],
            scaleX: [0.94, 1.08, 0.97],
            x: [0, 18, -8],
            y: [0, -6, 4],
          }}
          transition={{
            duration: 10 + index,
            delay: beam.delay,
            repeat: Infinity,
            repeatType: "mirror",
            ease: "easeInOut",
          }}
        />
      ))}

      <motion.div
        className="absolute left-[10%] top-[14%] h-36 w-36 rounded-full bg-[radial-gradient(circle,rgba(255,255,255,0.26),rgba(240,215,141,0.10),transparent_72%)] blur-3xl"
        animate={{ opacity: [0.1, 0.26, 0.12], scale: [0.95, 1.08, 0.98] }}
        transition={{ duration: 8, repeat: Infinity, repeatType: "mirror", ease: "easeInOut" }}
      />
      <motion.div
        className="absolute right-[10%] top-[20%] h-28 w-28 rounded-full bg-[radial-gradient(circle,rgba(255,255,255,0.22),rgba(240,215,141,0.08),transparent_72%)] blur-3xl"
        animate={{ opacity: [0.08, 0.2, 0.1], scale: [1, 1.08, 0.96] }}
        transition={{ duration: 9.5, repeat: Infinity, repeatType: "mirror", ease: "easeInOut" }}
      />
    </div>
  );
};