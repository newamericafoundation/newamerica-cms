
const linear = (t) => {
  return t;
}

const easeInQuad = (t) => {
  return t * t;
}

const easeOutQuad = (t) => {
  return t * (2 - t);
}

const easeInOutQuad = (t) => {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

const easeInCubic = (t) => {
  return t * t * t;
}

const easeOutCubic = (t) => {
  return (--t) * t * t + 1;
}

const easeInOutCubic = (t) => {
  return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
}

const easeInQuart = (t) => {
  return t * t * t * t;
}

const easeOutQuart = (t) => {
  return 1 - (--t) * t * t * t;
}

const easeInOutQuart = (t) => {
  return t < 0.5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t;
}

const easeInQuint = (t) => {
  return t * t * t * t * t;
}

const easeOutQuint = (t) => {
  return 1 + (--t) * t * t * t * t;
}

const easeInOutQuint = (t) => {
  return t < 0.5 ? 16 * t * t * t * t * t : 1 + 16 * (--t) * t * t * t * t;
}

export default {
  linear,
  easeInQuad,
  easeOutQuad,
  easeInOutQuad,
  easeInCubic,
  easeOutCubic,
  easeInOutCubic,
  easeInQuart,
  easeOutQuart,
  easeInOutQuart,
  easeInQuint,
  easeOutQuint,
  easeInOutQuint
};
