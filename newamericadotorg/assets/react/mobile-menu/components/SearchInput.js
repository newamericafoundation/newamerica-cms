import './SearchInput.scss';

import React from 'react';
import { Search } from '../../components/Icons';

const SearchInput = ({}) => (
  <div className="input">
    <form action="/search/?query=value" method="get">
      <Search />
      <input type="text" autoComplete="off" name="query" id="search-input" placeholder="Search" />
      <button type="submit" className="button--text with-caret--right">Go</button>
    </form>
  </div>
);

export default SearchInput;
