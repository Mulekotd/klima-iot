"use client";

import { useSetAtom } from "jotai";
import { useCallback, useEffect } from "react";
import { useDebouncedCallback } from "use-debounce";
import {
  lastRemoteCommandAtom,
  remoteFeedbackAtom,
  type RemoteControlCommand,
} from "@/state/atoms";

const REMOTE_COMMAND_DEBOUNCE_MS = 700;
const REMOTE_COMMAND_MAX_WAIT_MS = 2_000;

export function useDebouncedRemoteCommand() {
  const setFeedback = useSetAtom(remoteFeedbackAtom);
  const setLastCommand = useSetAtom(lastRemoteCommandAtom);

  const sendCommand = useDebouncedCallback(
    (command: RemoteControlCommand) => {
      // This atom is the integration boundary for the future IoT API mutation.
      setLastCommand(command);
      setFeedback("Comando sincronizado agora");
    },
    REMOTE_COMMAND_DEBOUNCE_MS,
    {
      leading: false,
      maxWait: REMOTE_COMMAND_MAX_WAIT_MS,
      trailing: true,
    },
  );

  useEffect(() => {
    return () => sendCommand.cancel();
  }, [sendCommand]);

  return useCallback(
    (command: RemoteControlCommand) => {
      setFeedback("Alterações aguardando envio...");
      sendCommand(command);
    },
    [sendCommand, setFeedback],
  );
}
