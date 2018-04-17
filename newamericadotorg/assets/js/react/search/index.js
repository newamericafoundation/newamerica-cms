import { Component } from 'react';
import { connect } from 'react-redux';
import getNestedState from '../../utils/get-nested-state';
import SearchBar from './components/Bar';
import SearchResults from './components/Results'
import SearchResultsPage from './components/ResultsPage';
import { NAME, ID } from './constants';
import { Fetch, Response } from '../components/API';

class APP extends Component {
  close = () => {
    this.props.dispatch({
      type: 'SET_SEARCH_STATE',
      component: 'site',
      state: false
    });
  }

  render(){
    let { page, index } = this.props;
    if(!this.props.active && page=='modal') return null;
    let name = `${NAME}.${index}`
    return (
      <section className={"search " + page}>
        {page=='modal' && <i className="fa fa-times" onClick={this.close}></i>}
        <div className={page=='search-page' ? 'container--medium' : 'container--narrow'}>
          <div className="container--medium content-filters">
            {page=='search-page' && <h1 className="centered">Search</h1>}
            <Fetch
              endpoint={'search'}
              name={name}
              fetchOnMount={false}
              eager={false}
              initialQuery={{
                page: 1,
                page_size: page=='search-page' ? 10 : 8,
                exclude_images: page=='search-page' ? false : true
              }}
              component={SearchBar}
              page={page} />
          </div>
          <Response
            name={name}
            showLoading={true}
            transition={true}
            component={page=='search-page' ? SearchResultsPage : SearchResults}/>
        </div>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  active: getNestedState(state, 'site.searchIsOpen')
});

APP = connect(mapStateToProps)(APP);

export default { APP, NAME, ID, MULTI: true };
