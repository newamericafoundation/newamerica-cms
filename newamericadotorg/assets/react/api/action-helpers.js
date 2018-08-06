import cache from '../cache';

export const parseResponse = (json) => {
  let results, hasNext, hasPrevious, page, count;
  if(json.results){
    results = json.results;
    hasNext = json.next!==null;
    hasPrevious = json.previous!==null;
    page = 1;
    count = json.count;
    let re = /.+page=([0-9]+)/;

    if(hasNext){
      let next = re.exec(json.next);
      page = next ? +next[1]-1 : 1;
    } else if(hasPrevious){
      let next = re.exec(json.previous);
      page = next ? +next[1]+1 : 2;
    }
  } else {
    results = json;
    hasNext = false;
    hasPrevious = false;
    page = 1;
    count = null;
  }

  if(json.error)
    console.log(json.error, json.message);

  return {
    hasNext, hasPrevious, page, results, count, error: json.error,
    message: json.message
  }
};

export const generateUrl = (params) => {
  let url = new URL(`${params.baseUrl}${params.endpoint}/`);
  for(let k in params.query)
    url.searchParams.append(k, params.query[k]);

    return url;
}

export const handleResponse = (response, dispatch, callback) => {



  
}
