import './Search.scss';

import React, { useState, useEffect } from 'react';
import * as QueryString from 'query-string';

import { PublicationListItem, Person } from '../../components/ContentCards';
import { LoadingDots } from '../../components/Icons';


function SearchResultList({results, header, bucket, hasNext, hasPrevious, fetchNext, fetchPrevious, fetchingNext, fetchingPrevious}) {
  // null is the initial state, and here we distinguish between "not
  // loaded yet" (null) and "no results" (empty list).
  if (results == null) {
    return <></>;
  }

  const onClickNext = e => {
    e.preventDefault();
    fetchNext();
  }

  const onClickPrevious = e => {
    e.preventDefault();
    fetchPrevious();
  }

  return (
    <div className={`search-results search-results--${bucket}`}>
      <h2>{header}</h2>

      {(results.length === 0)
        ? ("No results found.")
        : <div className="search-results__list">
            {results.map((result, i) => {
              if(result.content_type.api_name == 'person')
                return ( <Person key={`person-${result.id}`} person={result} /> );
              return ( <PublicationListItem key={`post-${result.id}`} post={result} style={(bucket=="programs") ? "search-small" : "search-large"} /> );
            })}
          </div>
      }
      <div class="search-results__pagination">
        {hasPrevious &&
        <div className="load-more load-more--previous">
          <button className={`button${fetchingPrevious ? ' is-fetching' : ''}`} onClick={onClickPrevious} disabled={fetchingPrevious}>
            <span className="load-more__label">Previous</span>
            {fetchingPrevious && <span className="loading-dots--absolute">
              <span>.</span><span>.</span><span>.</span>
            </span>}
          </button>
        </div>}

        {hasNext &&
        <div className="load-more">
          <button className={`button${fetchingNext ? ' is-fetching' : ''}`} onClick={onClickNext} disabled={fetchingNext}>
            <span className="load-more__label">Next</span>
            {fetchingNext && <span className="loading-dots--absolute">
              <span>.</span><span>.</span><span>.</span>
            </span>}
          </button>
        </div>}
      </div>
    </div>
  );
}

function SearchBucket({results, name, bucket, showEmpty, nextPaginationFilter, previousPaginationFilter, fetchNext, fetchingNext, fetchPrevious, fetchingPrevious}) {
  return (
    <div>
      {(showEmpty || (Array.isArray(results) && results.length > 1)) && <SearchResultList
        results={results}
        header={name}
        bucket={bucket}
        hasNext={!!nextPaginationFilter}
        fetchNext={fetchNext}
        hasPrevious={!!previousPaginationFilter}
        fetchPrevious={fetchPrevious}
        fetchingNext={fetchingNext}
        fetchingPrevious={fetchingPrevious}
       />}
    </div>
  )
}

function sortEmptyResultsToEnd(target1, target2) {
  let results1 = target1.results;
  let results2 = target2.results;

  if (!Array.isArray(results1) || (Array.isArray(results1) && results1.length === 0)) {
    return 1;
  }
  if (!Array.isArray(results2) || (Array.isArray(results2) && results2.length === 0)) {
    return -1;
  }

  return 0;
}

export default function Search({location, history}) {
  const {query} = QueryString.parse(location.search);

  const [queryInputValue, setQueryInputValue] = useState(query);
  const [results, setResults] = useState([]);
  const [isFetching, setIsFetching] = useState(false);

  const [searchTargets, setSearchTargets] = useState([
    {
      bucket: "programs",
      name: "Programs, Initiatives and Projects",
      endpoint: "/api/search/programs",
      showEmpty: true,
      pageSize: 6,
      nextPaginationFilter: null,
      previousPaginationFilter: null,
      paginationFilter: null,
      results: null,
      fetchingNext: false,
      fetchingPrevious: false,
    },
    {
      bucket: "upcoming_events",
      name: "Upcoming Events",
      endpoint: "/api/search/upcoming_events",
      showEmpty: true,
      pageSize: 6,
      nextPaginationFilter: null,
      previousPaginationFilter: null,
      paginationFilter: null,
      results: null,
      fetchingNext: false,
      fetchingPrevious: false,
    },
    {
      bucket: "pubs_and_past_events",
      name: "Publications and Past Events",
      endpoint: "/api/search/pubs_and_past_events",
      showEmpty: true,
      pageSize: 6,
      nextPaginationFilter: null,
      previousPaginationFilter: null,
      paginationFilter: null,
      results: null,
      fetchingNext: false,
      fetchingPrevious: false,
    },
    {
      bucket: "people",
      name: "People",
      endpoint: "/api/search/people",
      showEmpty: true,
      pageSize: 6,
      nextPaginationFilter: null,
      previousPaginationFilter: null,
      paginationFilter: null,
      results: null,
      fetchingNext: false,
      fetchingPrevious: false,
    },
    {
      bucket: "other",
      name: "Other Pages",
      endpoint: "/api/search/other",
      showEmpty: false,
      pageSize: 6,
      nextPaginationFilter: null,
      previousPaginationFilter: null,
      paginationFilter: null,
      results: null,
      fetchingNext: false,
      fetchingPrevious: false,
    },
  ]);

  const fetchTarget = target => {
    const params = {'page_size': target.pageSize}
    let queryString = '';

    if (query) {
      params['query'] = query;
    }
    if (target.paginationFilter) {
      Object.assign(params, target.paginationFilter);
    }
    if (params) {
      queryString = '?' + QueryString.stringify(params);
    }

    return fetch(`${target.endpoint}/${queryString}`)
      .then(response => response.json())
      .then(json => {

        const extractPaginationFilter = url => {
          if (url) {
            const parsedUrl = QueryString.parseUrl(url);
            const {query='', ...paginationFilter} = parsedUrl.query;

            return paginationFilter;
          } else {
            return null;
          }
        }

        return {
          ...target,
          results: json.results,
          nextPaginationFilter: extractPaginationFilter(json.next),
          previousPaginationFilter: extractPaginationFilter(json.previous),
        }
      });

  };

  useEffect(() => {
    setIsFetching(true);
    Promise.all(searchTargets.map(fetchTarget)).then(targetsWithResults => {
      setSearchTargets(targetsWithResults);
      setIsFetching(false);
    });
  }, [query]);

  const fetchNext = index => () => {
    let newTargets = [...searchTargets];
    let oldTarget = newTargets[index];
    oldTarget.paginationFilter = oldTarget.nextPaginationFilter;
    newTargets[index] = {...oldTarget, fetchingNext: true}; // update fetching state in UI
    setSearchTargets(newTargets);

    fetchTarget(oldTarget).then(updatedTarget => {
      updatedTarget.fetchingNext = false;
      let updatedTargets = [...searchTargets];
      updatedTargets[index] = updatedTarget;
      setSearchTargets(updatedTargets);
    })
  };

  const fetchPrevious = index => () => {
    let newTargets = [...searchTargets];
    let oldTarget = newTargets[index];
    oldTarget.paginationFilter = oldTarget.previousPaginationFilter;
    newTargets[index] = {...oldTarget, fetchingPrevious: true}; // update fetching state in UI
    setSearchTargets(newTargets);

    fetchTarget(oldTarget).then(updatedTarget => {
      updatedTarget.fetchingPrevious = false;
      let updatedTargets = [...searchTargets];
      updatedTargets[index] = updatedTarget;
      setSearchTargets(updatedTargets);
    })
  };

  // // Gets query params from state
  const getQueryParams = query => {
    const params = {};

    if (query) {
      params['query'] = query;
    }

    if (params) {
      return '?' + QueryString.stringify(params);
    } else {
      return '';
    }
  };

  console.log("RERENDER")

  // Trigger search when user presses the 'Enter' key
  const onKeyDownInSearchBox = e => {
    if (e.key === 'Enter') {
      history.push({
        pathname: location.pathname,
        search: getQueryParams(queryInputValue, null),
      });
    }
  };

  const onClickSearch = e => {
    e.preventDefault();

    history.push({
      pathname: location.pathname,
      search: getQueryParams(queryInputValue, null),
    });
  };

  const setPaginationFilter = newPaginationFilter => {
    history.push({
      pathname: location.pathname,
      search: getQueryParams(queryInputValue, newPaginationFilter),
    });
  };

  return (
    <div className="home__panels__search container">
      <div className="input margin-bottom-35">
        <input type="text" value={queryInputValue} name="query" onChange={e => setQueryInputValue(e.target.value)} onKeyDown={onKeyDownInSearchBox} required />
        <button className="button--text input__submit with-caret--right" onClick={onClickSearch}>Search</button>
      </div>

      {isFetching ? <LoadingDots /> : searchTargets.sort(sortEmptyResultsToEnd).map( (target, i) => {
        return (
          <SearchBucket
            key={i}
            query={query}
            bucket={target.bucket}
            name={target.name}
            showEmpty={target.showEmpty}
            results={target.results}
            nextPaginationFilter={target.nextPaginationFilter}
            previousPaginationFilter={target.previousPaginationFilter}
            fetchNext={fetchNext(i)}
            fetchPrevious={fetchPrevious(i)}
            fetchingNext={target.fetchingNext}
            fetchingPrevious={target.fetchingPrevious}
          />
        )})}
    </div>
  );
}
