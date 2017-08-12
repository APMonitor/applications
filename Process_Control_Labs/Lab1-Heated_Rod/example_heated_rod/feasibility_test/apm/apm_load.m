% APM Load Model File
function [response] = apm_load(server,app,filename)
   % load model
   fid=fopen(filename,'r');
   tline = [];
   while 1
      aline = fgets(fid);
      if ~ischar(aline), break, end
      tline = [tline aline];
   end
   fclose(fid);

   % send to server once for every 2000 characters
   ts = size(tline,2);
   block = 2000;
   cycles = ceil(ts/block);
   for i = 1:cycles,
      if i<cycles,
         apm_block = ['apm ' tline((i-1)*block+1:i*block)];
      else
         apm_block = ['apm ' tline((i-1)*block+1:end)];
      end       
      response = apm(server,app,apm_block);
   end
   response = 'Successfully loaded APM file';
   