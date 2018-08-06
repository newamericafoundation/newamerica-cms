import MockStore from 'redux-mock-store';
import fetch from 'jest-fetch-mock';
import thunk from 'redux-thunk';

const mockStore = MockStore([thunk]);

import { fetchData } from '../actions';

describe('testing fetching', () => {
  beforeEach(() => {
    fetch.resetMocks()
  });

  test('calls google and returns data to me', () => {
    const store = mockStore({
      fakeComponent: {
        params: {
          baseUrl: 'https://fake.io/',
          endpoint: '',
          query: {}
        }
      }
    });

    fetch.mockResponseOnce(JSON.stringify({
      count: 1,
      results: []
    }));

    let expectedActions = [
      'setFetchingStatus'
    ]
    //assert on the response
    return store.dispatch(fetchData('fakeComponent'))
      .then(() => {
        const actualActions = store.getActions().map(action => action.type);
        console.log(actualActions);
        expect(actualActions).to.eql(expectedActions)
     })

    //assert on the times called and arguments given to fetch
  //  expect(fetch.mock.calls.length).toEqual(1);
    //expect(fetch.mock.calls[0][0]).toEqual('https://google.com');
  });

});
