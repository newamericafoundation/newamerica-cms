import { Component } from 'react';
import { connect } from 'react-redux';
import getNestedState from '../../utils/get-nested-state';
import SearchBar from './components/Bar';
import SearchResults from './components/Results'
import { NAME, ID } from './constants';

class APP extends Component {

  render(){
    if(!this.props.active) return null;

    return (
      <section className="search">
        <div className="container--narrow">
          <SearchBar />
          <SearchResults />
        </div>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  active: getNestedState(state, 'site.searchIsOpen')
});

APP = connect(mapStateToProps)(APP);

export default { APP, NAME, ID };
