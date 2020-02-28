import './Search.scss';

import React, { useState, useEffect } from 'react';
import * as QueryString from 'query-string';

import { PublicationListItem, Person } from '../../components/ContentCards';
import { LoadingDots } from '../../components/Icons';

function SearchResultList({results, isFetching, hasNext, hasPrevious, fetchNext, fetchPrevious}) {
  // Remember if we've tried to fetch before
  // This helps us differentiate between the initial state and "No results"
  const [hasFetched, setHasFetched] = useState(false);
  const [fetchingNext, setFetchingNext] = useState(false);
  const [fetchingPrevious, setFetchingPrevious] = useState(false);
  useEffect(() => {
    if (isFetching) {
      setHasFetched(true);
    } else {
      setFetchingNext(false);
      setFetchingPrevious(false);
    }

  }, [isFetching]);

  if (!hasFetched) {
    return <></>;
  }

  if (results.length === 0) {
    // No results, display something to the user to explain why
    if (isFetching) {
      return (
        <div className="program__publications-list-wrapper">
          <div className="program__publications-list margin-top-60">
              <LoadingDots />
          </div>
        </div>
      );
    } else {
      return (
        <h4 className="centered">No results found</h4>
      );
    }
  }

  const onClickNext = e => {
    e.preventDefault();

    setFetchingNext(true);
    fetchNext();
  }

  const onClickPrevious = e => {
    e.preventDefault();

    setFetchingPrevious(true);
    fetchPrevious();
  }

  return (
    <div className="program__publications-list-wrapper">
      <div className="program__publications-list">
          {results.map((post, i) => {
            if(post.content_type.api_name == 'person')
              return ( <Person key={`post-${i}`} person={post} /> );
            return ( <PublicationListItem key={`post-${i}`} post={post} /> );
          })}
      </div>
      {hasPrevious &&
      <div className="program__publications-list-load-more margin-top-10" style={{float: 'left'}}>
        <button className={`button${fetchingPrevious ? ' is-fetching' : ''}`} onClick={onClickPrevious} disabled={isFetching}>
          <span className="load-more-label">Previous</span>
          {fetchingPrevious && <span className="loading-dots--absolute">
            <span>.</span><span>.</span><span>.</span>
          </span>}
        </button>
      </div>}
      {hasNext &&
      <div className="program__publications-list-load-more margin-top-10">
        <button className={`button${fetchingNext ? ' is-fetching' : ''}`} onClick={onClickNext} disabled={isFetching}>
          <span className="load-more-label">Next</span>
          {fetchingNext && <span className="loading-dots--absolute">
            <span>.</span><span>.</span><span>.</span>
          </span>}
        </button>
      </div>}
    </div>
  );
}

export default function Search({location, history}) {
  const {query: initialQuery='', ...initialPaginationFilter} = QueryString.parse(location.search);

  const [queryInputValue, setQueryInputValue] = useState(initialQuery || '');
  const [query, setQuery] = useState(initialQuery || '');
  const [results, setResults] = useState([]);
  const [isFetching, setIsFetching] = useState(false);

  // This contains any keys that the server has appended in next/previous URLs.
  // We don't care about what the pagination method is used here.
  // Example values could be:
  // - {page: 1, page_size: 20}
  // - {cursor: 'cD0yMDE4LTExLTE0LTIyMTc2'}
  const [paginationFilter, setPaginationFilter] = useState(initialPaginationFilter);

  // These contain the value of paginationFilter for the next/previous pages
  // null = next/prev page doesn't exist
  const [nextPaginationFilter, setNextPaginationFilter] = useState(null);
  const [previousPaginationFilter, setPreviousPaginationFilter] = useState(null);

  // Gets query params from state
  const getQueryParams = () => {
    const params = {};

    if (query) {
      params['query'] = encodeURIComponent(query);
    }

    if (paginationFilter) {
      Object.assign(params, paginationFilter);
    }

    if (params) {
      return '?' + QueryString.stringify(params);
    } else {
      return '';
    }
  };

  // Perform search when query changes
  useEffect(() => {
    const queryParams = getQueryParams();

    // Update URL in browser
    history.replace({
      pathname: location.pathname,
      search: queryParams,
    });

    if (query) {
      // Fetch results
      // TODO: Make sure responses come back in correct order
      setIsFetching(true);
      fetch(`/api/search/${queryParams}`)
      .then(response => response.json())
      .then(json => {
        setResults(json.results);
        setIsFetching(false);

        const extractPaginationFilter = url => {
          if (url) {
            const parsedUrl = QueryString.parseUrl(url);
            const {query='', ...paginationFilter} = parsedUrl.query;

            return paginationFilter;
          } else {
            return null;
          }
        }

        setNextPaginationFilter(extractPaginationFilter(json.next));
        setPreviousPaginationFilter(extractPaginationFilter(json.previous));
      });
    } else {
      setIsFetching(false);
      setResults([]);
      setNextPaginationFilter(null);
      setPreviousPaginationFilter(null);
    }
  }, [query, paginationFilter]);

  // Trigger search when user presses the 'Enter' key
  const onKeyDownInSearchBox = e => {
    if (e.key === 'Enter') {
      setQuery(queryInputValue);
      setPaginationFilter(null);
    }
  };

  const onClickSearch = e => {
    e.preventDefault();
    setQuery(queryInputValue);
    setPaginationFilter(null);
  };

  return (
    <div className="home__panels__search container">
      <div className="input margin-bottom-35">
        <input type="text" value={queryInputValue} name="query" onChange={e => setQueryInputValue(e.target.value)} onKeyDown={onKeyDownInSearchBox} required />
        <h5 className="input__label">
          <label htmlFor="query">Search</label>
        </h5>
      </div>

      <button class="button" onClick={onClickSearch}>Search</button>

      <SearchResultList
        results={results}
        isFetching={isFetching}
        hasNext={!!nextPaginationFilter}
        fetchNext={() => setPaginationFilter(nextPaginationFilter)}
        hasPrevious={!!previousPaginationFilter}
        fetchPrevious={() => setPaginationFilter(previousPaginationFilter)}
      />
    </div>
  );
}
