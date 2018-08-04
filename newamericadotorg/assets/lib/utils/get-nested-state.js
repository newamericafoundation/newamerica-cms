/**
  Recursively find object in nested state with string 'parent.child.grandchild';
**/

const getNestedState = (state, name) => {
  let i = name.indexOf('.');
  if(i===-1) return state[name] || undefined;
  return getNestedState(state[name.slice(0,i)] || {}, name.slice(i+1,name.length));
}

export default getNestedState;
