# Docker Qdrant Troubleshooting Guide

This guide helps resolve Docker-related issues with the Qdrant container.

---

## Common Issue: Container Exits with Error 101

### Symptoms
```
ERROR: Qdrant did not start within expected time
Container Status: Exited (101)
```

### Root Causes

1. **Corrupted Data** - Most common issue
   - Error in logs: `OutputTooSmall { expected: 4, actual: 0 }`
   - Error in logs: `failed to deduplicate points`
   
2. **Filesystem Incompatibility**
   - Warning: `Unrecognized filesystem - cannot guarantee data safety`
   - Common with network drives, USB drives, or certain cloud storage

3. **Port Conflict**
   - Port 6333 already in use by another service

---

## Quick Fix: Remove and Recreate

### Option 1: Using the Improved Batch File

The updated `start_mcp_server.bat` now includes interactive prompts:

```batch
start_mcp_server.bat
```

When prompted:
- **Found container with error?** → Choose `(N)remove and recreate`
- **Found existing data?** → Choose `(C)clean data directory` if corrupted

### Option 2: Manual Cleanup

```powershell
# Stop and remove container
docker rm -f qdrant-mcp

# Clean data directory (WARNING: Deletes all data!)
rd /s /q I:\qdrant_data

# Recreate data directory
mkdir I:\qdrant_data

# Start fresh container
docker run -d --name qdrant-mcp -p 6333:6333 -v ./qdrant_data:/qdrant/storage qdrant/qdrant

# Verify it's running
docker ps
curl http://localhost:6333/healthz
```

---

## Improved Batch File Features

The updated `start_mcp_server.bat` now includes:

### 1. **Existing Container Detection**
- Detects if port 6333 is already in use
- Finds running Qdrant containers (any name)
- Option to use existing container

### 2. **Error Detection**
- Checks if container exited with error
- Shows container logs when errors found
- Prompts for action (start/remove/view logs)

### 3. **Data Corruption Handling**
- Warns about existing data
- Options to:
  - Use existing data
  - Create fresh container (no data mount)
  - Clean data directory

### 4. **Better Error Messages**
- Shows container status and logs on failure
- Provides troubleshooting steps
- Lists common issues and solutions

---

## Understanding the Data Corruption Issue

### What Happened

The Qdrant container crashed because:

1. **Initial Error**: 
   ```
   Filesystem check failed for storage path ./storage
   Unrecognized filesystem - cannot guarantee data safety
   ```
   - The data drive uses a filesystem Qdrant didn't recognize
   - This is usually safe but Qdrant warned about it

2. **Loading Collection**:
   ```
   Loading collection: your-collection-name
   ```
   - Qdrant tried to load an existing collection

3. **Corruption Detected**:
   ```
   OutputTooSmall { expected: 4, actual: 0 }
   ```
   - Collection data files were corrupted
   - Likely from improper shutdown or filesystem incompatibility

4. **Crash**:
   ```
   Exited (101)
   ```
   - Qdrant couldn't recover and shut down

### Prevention

1. **Use Local Drive** (Recommended):
   ```batch
   set QDRANT_DATA_PATH=%LOCALAPPDATA%\qdrant_data
   ```
   Better than network or USB drives.

2. **Proper Shutdown**:
   ```powershell
   # Stop gracefully
   docker stop qdrant-mcp
   
   # NOT force kill unless necessary
   # docker rm -f qdrant-mcp  # Avoid this when possible
   ```

3. **Regular Backups**:
   ```powershell
   # Backup data directory
   xcopy /E /I /H I:\qdrant_data I:\qdrant_data_backup
   ```

---

## Checking Container Status

### View Running Containers
```powershell
docker ps
```

### View All Containers (including stopped)
```powershell
docker ps -a
```

### View Container Logs
```powershell
# Last 50 lines
docker logs --tail 50 qdrant-mcp

# Follow logs in real-time
docker logs -f qdrant-mcp

# All logs
docker logs qdrant-mcp
```

### Check Container Health
```powershell
# Container status
docker ps -a --filter "name=qdrant-mcp" --format "{{.Status}}"

# Qdrant health
curl http://localhost:6333/healthz

# Qdrant collections
curl http://localhost:6333/collections
```

---

## Port Conflict Resolution

### Check What's Using Port 6333
```powershell
netstat -ano | findstr :6333
```

### Find Process Details
```powershell
# Get PID from netstat output, then:
tasklist /FI "PID eq <pid>"
```

### Stop Conflicting Process
```powershell
# If it's another Docker container
docker stop <container-name>

# If it's a Windows process
taskkill /F /PID <pid>
```

---

## Data Location Options

### Option 1: Local AppData (Recommended)
```batch
set QDRANT_DATA_PATH=%LOCALAPPDATA%\qdrant_data
```
**Pros**: Fast, reliable filesystem  
**Cons**: Local to this machine only

### Option 2: Project Directory
```batch
set QDRANT_DATA_PATH=%~dp0qdrant_data
```
**Pros**: Keeps data with project  
**Cons**: Same drive as code

### Option 3: Custom Path
```batch
set QDRANT_DATA_PATH=C:\data\qdrant
```
**Pros**: Full control  
**Cons**: Manual management

### Option 4: Docker Volume (No Persistence Between Machines)
```powershell
# Don't mount host directory
docker run -d --name qdrant-mcp -p 6333:6333 qdrant/qdrant
```
**Pros**: No filesystem issues  
**Cons**: Data lost when container removed

---

## Testing After Fix

### 1. Verify Container is Running
```powershell
docker ps | findstr qdrant
```
Expected output:
```
qdrant-mcp   qdrant/qdrant   Up X minutes   0.0.0.0:6333->6333/tcp
```

### 2. Check Qdrant Health
```powershell
curl http://localhost:6333/healthz
```
Expected output: `200 OK` or similar

### 3. List Collections
```powershell
curl http://localhost:6333/collections
```

### 4. Run MCP Server
```powershell
start_mcp_server.bat
```
Should see: `Qdrant is ready!`

---

## Best Practices

### 1. Container Management
- Use `docker stop` instead of `docker rm -f` when possible
- Check logs before removing failed containers
- Keep container names consistent

### 2. Data Management
- **Backup before major changes**
- Use local drives when possible
- Monitor disk space
- Clean old data periodically

### 3. Startup Routine
1. Run `start_mcp_server.bat`
2. Read prompts carefully
3. Check logs if errors occur
4. Don't force actions without understanding

### 4. When to Clean Data
- After multiple failed starts
- When seeing corruption errors
- Before major Qdrant version upgrades
- When changing data location

---

## Emergency Recovery

### Complete Reset
```powershell
# 1. Stop and remove container
docker rm -f qdrant-mcp

# 2. Backup data (optional but recommended)
xcopy /E /I /H I:\qdrant_data I:\qdrant_data_backup

# 3. Clean data directory
rd /s /q I:\qdrant_data
mkdir I:\qdrant_data

# 4. Start fresh
start_mcp_server.bat
```

### Recover from Backup
```powershell
# 1. Stop container
docker stop qdrant-mcp

# 2. Restore data
rd /s /q I:\qdrant_data
xcopy /E /I /H I:\qdrant_data_backup I:\qdrant_data

# 3. Restart container
docker start qdrant-mcp
```

---

## Common Error Messages

### "Port is already allocated"
**Cause**: Port 6333 in use  
**Fix**: Stop other container or change port

### "No such container"
**Cause**: Container doesn't exist  
**Fix**: Let batch file create new one

### "Exited (101)"
**Cause**: Qdrant crashed (usually data corruption)  
**Fix**: Remove container and clean data

### "Permission denied"
**Cause**: Docker daemon not running or no permissions  
**Fix**: Start Docker Desktop, run as administrator

### "Cannot connect to Docker daemon"
**Cause**: Docker not running  
**Fix**: Start Docker Desktop

---

## Advanced: Custom Qdrant Configuration

### Using Custom Config File
```powershell
# Create config.yaml
# Mount it to container
docker run -d --name qdrant-mcp -p 6333:6333 `
  -v ./qdrant_data:/qdrant/storage `
  -v ./qdrant_config.yaml:/qdrant/config/production.yaml `
  qdrant/qdrant
```

### Setting Memory Limits
```powershell
docker run -d --name qdrant-mcp -p 6333:6333 `
  --memory=2g `
  -v ./qdrant_data:/qdrant/storage `
  qdrant/qdrant
```

---

## Related Documentation

- **Main Troubleshooting**: `TROUBLESHOOTING.md` - General MCP issues
- **Configuration**: `CONFIG.md` - Server configuration
- **Debugging**: `DEBUGGING_GUIDE.md` - Deep debugging process

---

## Quick Reference

| Issue | Command | Documentation |
|-------|---------|---------------|
| Container won't start | `docker logs qdrant-mcp` | See logs section |
| Port conflict | `netstat -ano \| findstr :6333` | Port Conflict Resolution |
| Data corruption | `rd /s /q I:\qdrant_data` | Data Corruption Handling |
| Complete reset | See Emergency Recovery | Emergency Recovery section |

---

**Last Updated**: October 21, 2024

