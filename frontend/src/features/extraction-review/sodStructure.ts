export type SodBlock =
  | { kind: "heading"; text: string }
  | { kind: "narrative"; text: string }
  | { kind: "point"; marker: string; level: number; text: string };

const POINT_MARKER = /^(\d+|[A-Z]|[a-z]|[ivxlcdm]+)[.)]\s+(.+)$/;
const HEADING = /^(?:findings include|facility policy|medical record review|interviews):$/i;

export function structureSodText(value: string): readonly SodBlock[] {
  const blocks: SodBlock[] = [];
  let activeBlock: SodBlock | null = null;

  function flushActiveBlock() {
    if (activeBlock) {
      blocks.push(activeBlock);
      activeBlock = null;
    }
  }

  for (const rawLine of value.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line) {
      flushActiveBlock();
      continue;
    }

    if (HEADING.test(line)) {
      flushActiveBlock();
      blocks.push({ kind: "heading", text: line });
      continue;
    }

    const point = POINT_MARKER.exec(line);
    if (point) {
      flushActiveBlock();
      const marker = point[1];
      activeBlock = {
        kind: "point",
        marker: `${marker}.`,
        level: pointLevel(marker),
        text: point[2],
      };
      continue;
    }

    if (activeBlock) {
      activeBlock = { ...activeBlock, text: `${activeBlock.text} ${line}` };
    } else {
      activeBlock = { kind: "narrative", text: line };
    }
  }

  flushActiveBlock();
  return blocks;
}

function pointLevel(marker: string): number {
  if (/^\d+$/.test(marker)) return 1;
  if (/^[A-Z]$/.test(marker)) return 2;
  if (/^[ivxlcdm]+$/.test(marker)) return 3;
  return 4;
}

export function pointLevelFromLabel(label: string): number {
  return pointLevel(label.replace(/[.)]\s*$/, ""));
}