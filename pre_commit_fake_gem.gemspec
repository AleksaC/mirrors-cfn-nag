Gem::Specification.new do |s|
    s.name = 'pre_commit_fake_gem'
    s.executables << 'cfn_nag_scan_wrapper'
    s.version = '0.0.0'
    s.authors = ['Aleksa Cukovic']
    s.summary = 'A fake mirror gem for cfn nag'
    s.description = 'A fake mirror gem for cfn nag'
    s.add_dependency 'cfn-nag', '0.7.7'
end
