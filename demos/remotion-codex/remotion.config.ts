import {Config} from '@remotion/cli/config';

// Leave unset to use Remotion's default browser on other machines.
if (process.env.REMOTION_BROWSER_EXECUTABLE) {
  Config.setBrowserExecutable(process.env.REMOTION_BROWSER_EXECUTABLE);
}
