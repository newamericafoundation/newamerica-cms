export default function(list, key) {
  return list.reduce(function(val, x) {
    (val[x[key]] = val[x[key]] || []).push(x);
    return val;
  }, {});
};
