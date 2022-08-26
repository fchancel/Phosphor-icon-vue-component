<script setup lang="ts">
import { computed } from "vue";
import { importSvg } from "@/icons/importSvg";

interface Props {
  icon: string;
  size?: "sm" | "md" | "lg" | "xl" | "xl2" | "xl3"; //par défault = lg
  strokeWidth?: "sm" | "md" | "lg"; // par defaut = md
  fillColor?: string; // the colors must be expressed by tailwind classes : fill-white
  strokeColor?: string; // the colors must be expressed by tailwind classes : stroke-white
}

const props = withDefaults(defineProps<Props>(), {
  strokeWidth: "md",
  size: "lg",
  strokeColor: "stroke-light",
  fillColor: undefined,
});

const IconComponent = importSvg(props.icon);

const getStrokeWidth = computed(() => {
  return `stroke-${props.strokeWidth}`;
});
</script>

<template>
  <span>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 256 256"
      :aria-labelledby="icon"
      :class="[size, getStrokeWidth, strokeColor, fillColor]"
      v-html="IconComponent"
    ></svg>
  </span>
</template>

<style>
.xs {
  height: 20px;
  width: 20px;
}

.sm {
  height: 20px;
  width: 20px;
}

.md {
  height: 24px;
  width: 24px;
}

.lg {
  height: 28px;
  width: 28px;
}

.xl {
  height: 32px;
  width: 32px;
}

.xl2 {
  height: 36px;
  width: 36px;
}

.xl3 {
  height: 40px;
  width: 40px;
}

.stroke-sm {
  @apply stroke-[10px];
}

.stroke-md {
  @apply stroke-[16px];
}

.stroke-lg {
  @apply stroke-[24px];
}
</style>
