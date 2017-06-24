/**
Get all data- properties from html element
**/

import camelize from './camelize';

const getProps = function(el){
  let props = {};
  for(let i=0; i<el.attributes.length; i++){
    let attr = el.attributes[i],
    name = attr.nodeName,
    val = attr.nodeValue;
    if(name.indexOf('data-')!==-1){
      props[camelize(name.replace('data-',''))] = val;
    }
  }
  return props;
}

export default getProps;
