from _utils import *
import _utils

globaldir = None


def main():
    """Main entry point for the cursor shadow patch."""
    print(
        f"""
{RED}<== {PURPLE}[{RESET}Cursor Shadow Patch{PURPLE}]{RED} ==>{RESET}

- Custom machine id, mac address, etc."""
    )

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if SYSTEM == "Linux":
        appimage = appimagepath("")
        appimage_unpacked = appimage_unpack(appimage)
        js = jspath(appimage_detect_jspath(appimage_unpacked))
    else:
        appimage = appimage_unpacked = None
        js = jspath("")
    data = load(js)
    is_patched = chk(data, [b"/*csp1*/", b"/*csp2*/", b"/*csp3*/", b"/*csp4*/"])

    machineid = randomuuid("")
    # async function machineId(returnRaw) {
    #     let machineid = processOutput(execSync(commands[PLATFORM], { timeout: 5e3 }).toString()),
    #         hash;
    #     try {
    #         hash = (await import("crypto")).createHash("sha256").update(machineid, "utf8").digest("hex");
    #     } catch {
    #         hash = uuid();
    #     }
    #     return returnRaw ? machineid : hash;
    # }
    data = replace(
        data,
        r"=.{0,50}timeout.{0,10}5e3.*?,",
        f'=/*csp1*/"{machineid}"/*1csp*/,',
        r"=/\*csp1\*/.*?/\*1csp\*/,",
    )

    mac = macaddr("")
    # function getMacAddress() {
    #     const interfaces = networkInterfaces();
    #     for (const name in interfaces) {
    #         const details = interfaces[name];
    #         if (details) {
    #             for (const { mac: m } of details) if (isValidMac(m)) return m;
    #         }
    #     }
    #     throw new Error("Unable to retrieve mac address (unexpected format)");
    # }
    data = replace(
        data,
        r"(function .{0,50}\{).{0,300}Unable to retrieve mac address.*?(\})",
        f'\\1return/*csp2*/"{mac}"/*2csp*/;\\2',
        r"()return/\*csp2\*/.*?/\*2csp\*/;()",
    )

    sqm = ""
    # async function sqmId(errorBind) {
    #     if (isWindows) {
    #         const reg = await import("@vscode/windows-registry");
    #         try {  // REGPATH = "Software\\Microsoft\\SQMClient"
    #             return (reg.GetStringRegKey("HKEY_LOCAL_MACHINE", REGPATH, "MachineId") || "");
    #         } catch (e) {
    #             return errorBind(e), "";
    #         }
    #     }
    #     return "";
    # }
    data = replace(
        data,
        r'return.{0,50}\.GetStringRegKey.*?HKEY_LOCAL_MACHINE.*?MachineId.*?\|\|.*?""',
        f'return/*csp3*/"{sqm}"/*3csp*/',
        r"return/\*csp3\*/.*?/\*3csp\*/",
    )

    devid = randomuuid("")
    # async function devDeviceId(errorBind) {
    #     try {
    #         return await (await import("@vscode/deviceid")).getDeviceId();
    #     } catch (e) {
    #         return errorBind(e), uuid();
    #     }
    # }
    data = replace(
        data,
        r"return.{0,50}vscode\/deviceid.*?getDeviceId\(\)",
        f'return/*csp4*/"{devid}"/*4csp*/',
        r"return/\*csp4\*/.*?/\*4csp\*/",
    )

    # Preprocess App Bundle for macOS
    if SYSTEM == "Darwin":
        appbundle = appbundle_from_jspath(js)
        backup(appbundle, not is_patched)
        appbundle_tmp = appbundle_movetmp(appbundle)
        appbundle_unsign(appbundle_tmp)
        js = appbundle_to_jspath(appbundle_tmp)
    else:
        appbundle = appbundle_tmp = None

    # Try to fix permissions for Windows
    if SYSTEM == "Windows":
        remove_readonly(js.parent)
        remove_readonly(js)

    # Backup and save
    backup(js, not is_patched)
    save(js, data)

    # Postprocess App Bundle for macOS
    if SYSTEM == "Darwin":
        assert appbundle is not None
        assert appbundle_tmp is not None
        appbundle_sign(appbundle_tmp)
        appbundle_moveback(appbundle_tmp, appbundle)

    # Pack AppImage for Linux
    if SYSTEM == "Linux":
        assert appimage is not None
        assert appimage_unpacked is not None
        backup(appimage, not is_patched)
        appimage_repack(appimage, appimage_unpacked)

    # Clean Temporary Files
    def cleantmp(filesglob=["cache*", "*onfig"]):
        """clean cache-* and .config files"""
        if not globaldir or not globaldir.exists():
            return
        assert globaldir
        for glob in filesglob:
            for file in globaldir.glob(glob):
                try:
                    file.unlink()
                except Exception as e:
                    print(f"{RED}[ERR] Failed to delete {file}: {e}{RESET}")

    _utils.cleantmp = cleantmp  # type:ignore

    match SYSTEM:
        case "Windows":
            tmp = path(os.getenv("APPDATA", "")) / "Cursor"
        case "Linux":
            tmp = path(os.getenv("HOME", "")) / ".config" / "Cursor"
        case "Darwin":
            tmp = (
                path(os.getenv("HOME", ""))
                / "Library"
                / "Application Support"
                / "Cursor"
            )
        case _:
            print(f"{RED}[ERR] Unsupported OS: {SYSTEM}{RESET}")
            pause()
            exit()
    clean_tmp(tmp)

    pause()


if __name__ == "__main__":
    main()
