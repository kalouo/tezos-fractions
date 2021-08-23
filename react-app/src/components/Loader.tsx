import { ClipLoader } from 'react-spinners';
import { css } from '@emotion/react';

const override = css`
  margin: 0 auto;
`;

const Loader = ({ loading }: { loading: boolean }) => <ClipLoader css={override} loading={loading} />;

export default Loader;
