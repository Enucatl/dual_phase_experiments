require "csv"
require "rake/clean"

datasets = CSV.table "datasets.csv"


def reconstructed_from_raw sample, flat
  file1 = File.basename(sample, ".*")
  file2 = File.basename(flat, ".*")
  dir = File.dirname(sample)
  File.join(dir, "#{file1}_#{file2}.h5")
end


def cropped_from_reconstructed reconstructed
  dirname = File.dirname(reconstructed)
  new_filename = File.basename(reconstructed, ".h5") + "_cropped.h5"
  File.join(dirname, new_filename)
end


datasets[:reconstructed] = datasets[:sample].zip(
  datasets[:flat]).map {|s, f| reconstructed_from_raw(s, f)}
datasets[:cropped] = datasets[:reconstructed].map {|f| cropped_from_reconstructed(f)}


namespace :reconstruction do

  datasets.each do |row|
    reconstructed = row[:reconstructed]
    CLEAN.include(reconstructed)

    desc "dpc_reconstruction of #{reconstructed}"
    file reconstructed => [row[:sample], row[:flat]] do |f|
      Dir.chdir "../dpc_reconstruction" do
        sh "dpc_radiography --drop_last --group /entry/data/threshold_0 #{f.prerequisites[0]} #{f.prerequisites[1]}"
      end
    end
  end

  file "reconstructed.csv" => datasets[:reconstructed] do |f|
    File.open(f.name, "w") do |file|
      file.write(datasets.to_csv)
    end
  end
  CLOBBER.include("source/data/reconstructed.csv")

  desc "reconstruct all"
  task :all => "reconstructed.csv"

end


namespace :postprocessing do

  datasets.each do |row|
    desc "crop of #{row[:reconstructed]}"
    file row[:cropped] => ["crop.py", row[:reconstructed]] do |f|
      sh "python #{f.source} #{f.prerequisites[1]} #{f.name} --roi 0 -1 0 -1"
    end
    CLEAN.include(row[:cropped])

  end

  desc "crop all"
  task :crop => datasets[:cropped]

  stacked = File.join(
    File.dirname(datasets[:reconstructed][0]),
    "stacked.h5")

  desc "stack"
  file stacked => ["stack.py"] + datasets[:cropped] do |f|
    sh "python #{f.source} #{f.prerequisites.drop(1).join(" ")} #{f.name}"
  end

  CLEAN.include(stacked)

end
