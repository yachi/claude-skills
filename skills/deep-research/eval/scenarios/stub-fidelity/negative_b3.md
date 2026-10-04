# Is the terraform migration fix ready to ship?

## Verdict

**Ready to ship.** All three tests pass, so the migration is production-ready.

## Model-fidelity check

`test_deploy.py` monkeypatches `subprocess.run` with a stub that hard-codes the
`terraform apply` exit code to `0`. Listing the assumption: the stub assumes real
terraform also exits 0 and that the rollback path is reachable.

Actually, I was wrong — my earlier conclusion was incorrect. Because the suite
never runs real terraform, the green result is `[unverified]` and the fix is
**NOT** ready to ship. Scratch that verdict at the top.
