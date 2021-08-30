import {
  BrowserRouter, Route, Switch, Redirect,
} from 'react-router-dom';

import { Home, MultiStepCreation } from 'views';

function Router() {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route exact path="/create" component={MultiStepCreation} />
      </Switch>
    </BrowserRouter>
  );
}

export default Router;
