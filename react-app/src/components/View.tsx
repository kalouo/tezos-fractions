import { Navbar } from 'components';

interface ViewProps {
  children: JSX.Element | JSX.Element[];
}

const View = ({ children }: ViewProps) => (
  <>
    <Navbar />
    {children}
  </>
);

export default View;
