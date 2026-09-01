const ACCEPTED_LINE=/FLEET_RX propagation=accepted mode=command/;

export function createP2PSeedRuntime({delay=ms=>new Promise(resolve=>setTimeout(resolve,ms)),bootSettleMs=5000,timeoutMs=5000}={}) {
  let binding=null;
  function bind({port,token,targetId,verified}) {
    if(!verified||targetId!=="quinled-dig2go"||!port?.getInfo||!token) return null;
    binding=Object.freeze({port,token,targetId,portInfo:Object.freeze({...port.getInfo()})});
    return binding;
  }
  async function seed(candidate,{onStatus=()=>{}}={}) {
    if(!binding||candidate!==binding)throw Error("The verified Dig2Go session is stale; install or verify it again");
    const info=binding.port.getInfo();if(info.usbVendorId!==binding.portInfo.usbVendorId||info.usbProductId!==binding.portInfo.usbProductId)throw Error("The connected USB device changed; seed was not started");
    const port=binding.port;onStatus("Opening the verified Dig2Go serial session…");await port.open({baudRate:115200});let reader;
    try {
      // CP210x control-line changes can reset a Dig2Go when Web Serial opens it.
      // Do not transmit into the bootloader/rescue window; allow Tubes setup to
      // reach Controller: ok before sending the local FleetUpdateOffer trigger.
      onStatus("Waiting for the Dig2Go firmware to finish starting…");
      await delay(bootSettleMs);
      reader=port.readable.getReader();
      const writer=port.writable.getWriter();await writer.write(new TextEncoder().encode("P!\n"));writer.releaseLock();onStatus("Propagation command sent. Waiting for the Dig2Go to accept one serve turn.");const timeout=delay(timeoutMs).then(()=>({timeout:true}));let text="";while(text.length<8192){const result=await Promise.race([reader.read(),timeout]);if(result.timeout||result.done)break;text+=new TextDecoder().decode(result.value||new Uint8Array());if(ACCEPTED_LINE.test(text))return {status:"sent",acknowledged:true,retryable:false};}return {status:"sent",acknowledged:false,retryable:true};
    } finally {try{await reader?.cancel();}catch{}try{reader?.releaseLock();}catch{}try{await port.close();}catch{}binding=null;}
  }
  return {bind,seed};
}
